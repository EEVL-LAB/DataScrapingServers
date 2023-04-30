import io
import zlib
import logging
import aiohttp
from tqdm import tqdm
from kafka_producer import *


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


available_keys = [
    'TITLE',
    'DATE',
    'CONTENT',
    'IMAGE_URL'
]


async def extract_crc_from_string(string: str) -> int:
    bytes_string = bytes(string, encoding='utf8')
    return zlib.crc32(bytes_string)


async def request_news_list(target_keyword: str, start_date: str, end_date: str, limit: int):
    url = f'https://www.bigkinds.or.kr/news/subMainData.do?pageInfo=mainNews&login_chk=&LOGIN_SN=&LOGIN_NAME=&indexName=news&keyword={target_keyword}&byLine=&searchScope=1&searchFtr=3&startDate={start_date}&endDate={end_date}&sortMethod=date&contentLength=100&providerCode=&categoryCode=&incidentCode=&dateCode=&highlighting=false&sessionUSID=&sessionUUID=test&listMode=&categoryTab=&newsId=&delnewsId=&delquotationId=&delquotationtxt=&filterProviderCode=&filterCategoryCode=&filterIncidentCode=&filterDateCode=&filterAnalysisCode=&startNo=1&resultNumber={limit}&topmenuoff=&resultState=newsSubMain&keywordJson=&keywordFilterJson=&realKeyword=&keywordYn=Y&totalCount=&interval=&quotationKeyword1=&quotationKeyword2=&quotationKeyword3=&printingPage=&searchFromUseYN=N&searchFormName=&searchFormSaveSn=&mainTodayPersonYn=&period=&sectionDiv='
    headers = {
            "Host": "www.bigkinds.or.kr",
            "Connection": "keep-alive",
            "sec-ch-ua": '''"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"''',
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.bigkinds.or.kr/v2/news/recentNews.do"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.get(
            url=url,
        )
        response = await response.json()
        responses = response.get("resultSet").get('resultList')
        result = list()
        producer = await initialize_producer()
        await producer.start()
        pbar = tqdm(responses, file=tqdm_out)
        for response in pbar:
            date = response.get('DATE')
            date = f'{date[:4]}-{date[4:6]}-{date[6:]}'
            content_plain_text = response.get('CONTENT').replace('\n', ' ')
            post = {
                'url': response.get('PROVIDER_LINK_PAGE'),
                'date': date,
                'title': response.get('TITLE'),
                'contents': response.get('CONTENT'),
                'content_plain_text': content_plain_text,
                'thumbnails': [response.get('IMAGE_URL')],
                'target_keyword': target_keyword,
                'channel_keyname': 'bigkinds',
                'crc': await extract_crc_from_string(content_plain_text)
            }
            await send(producer, 'scraping', post)
            result.append(post)
            pbar.set_postfix(channel='bigkinds', target_keyword=target_keyword, date=date)
        await producer.stop()
        return result
