import io
import json
import aiohttp
import logging
import zlib
from urllib import parse
from scraping.fiddler.utils import sanitize_html
from bs4 import BeautifulSoup as bs
from kafka_producer import *
from aiokafka import AIOKafkaProducer
from tqdm.asyncio import tqdm


class TqdmToLogger(io.StringIO):
    """
    Output stream for TQDM which will output to logger module instead of the StdOut.
    """
    logger = None
    level = None
    buf = ''
    def __init__(self,logger,level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO
        
    def write(self,buf):
        self.buf = buf.strip('\r\n\t ')
        
    def flush(self):
        self.logger.log(self.level, self.buf)
        
        
logging.basicConfig(format='%(asctime)s [%(levelname)-8s] %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
tqdm_out = TqdmToLogger(logger,level=logging.INFO)


async def request_search_list(
        target_keyword: str,
        start_date: str, 
        end_date: str, 
        current_page: int
    ) -> str:
    encoded_keyword = parse.quote(target_keyword)
    url = f'https://section.blog.naver.com/ajax/SearchList.naver?countPerPage=7&currentPage={current_page}&endDate={end_date}&keyword={encoded_keyword}&orderBy=sim&startDate={start_date}&type=post'
    headers = {
        "Host":"section.blog.naver.com",
        "Connection":"keep-alive",
        "Accept":"application/json, text/plain, */*",
        "Referer":f'https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword={encoded_keyword}',
    }
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url=url,
            headers=headers
        )
        response_string = await response.text()
        return response_string
    

async def extract_information_from_search_results(
    target_keyword: str, 
    start_date: str, 
    end_date: str, 
    current_page: int
):
    response_string = await request_search_list(
        target_keyword=target_keyword,
        start_date=start_date,
        end_date=end_date,
        current_page=current_page
    )
    response_string = response_string.split('\n')[1]
    response_dict = json.loads(response_string)
    total_count = response_dict.get('result').get('totalCount')
    search_results = response_dict.get('result').get('searchList')
    return total_count, search_results


async def extract_crc_from_string(string: str) -> int:
    bytes_string = bytes(string, encoding='utf8')
    return zlib.crc32(bytes_string)


async def request_post_list(producer: AIOKafkaProducer, target_keyword: str, start_date: str, end_date: str, current_page: int=0) -> list:
    total_count, search_results = await extract_information_from_search_results(
        target_keyword=target_keyword,
        start_date=start_date,
        end_date=end_date,
        current_page=current_page
    )
    post_list = list()
    pbar = tqdm(search_results, file=tqdm_out)
    for search_result in pbar:
        content_plain_text = await request_post_content(search_result.get('postUrl'))
        post = {
                    'url': search_result.get('postUrl'),
                    'title': search_result.get('noTagTitle', await sanitize_html(search_result.get('title'))),
                    'contents': await sanitize_html(search_result.get('contents')),
                    'content_plain_text': content_plain_text,
                    'thumbnails': [thumbnail.get('url') for thumbnail in search_result.get('thumbnails')],
                    'target_keyword': target_keyword,
                    'channel_keyname': 'naver-blog',
                    'crc': await extract_crc_from_string(content_plain_text)
                }
        await send(producer, 'scraping', post)
        post_list.append(post)
        pbar.set_postfix(target_keyword=target_keyword, page=current_page)
    return post_list


async def request_post_content(url: str):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        response_string = await response.text()
        soup = bs(response_string, "html.parser")
        frame = soup.find('iframe', id='mainFrame')
        frame_addr = 'https://blog.naver.com/' + frame['src']
        response = await session.get(frame_addr)
        response_string = await response.text()
        soup = bs(response_string, "lxml") 

    if soup.find("div", attrs={"class":"se-main-container"}):
        text = soup.find("div", attrs={"class":"se-main-container"}).get_text()
        text = text.replace("\n","") #공백 제거
        return text
    return 'None'
