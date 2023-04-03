import json
import aiohttp
from urllib import parse
from scraping.fiddler.utils import sanitize_html
from bs4 import BeautifulSoup as bs
from kafka_producer import *


async def request_post_list(target_keyword: str, start_date: str, end_date: str, current_page: int=0) -> list:

    async def request_search_list(target_keyword: str) -> str:
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

    response_string = await request_search_list(target_keyword=target_keyword)
    response_string = response_string.split('\n')[1]
    response_dict = json.loads(response_string)
    search_results = response_dict.get('result').get('searchList')
    post_list = list()
    producer = await initialize_producer()
    await producer.start()
    for search_result in search_results:
        post = {
                    'url': search_result.get('postUrl'),
                    'title': search_result.get('noTagTitle', sanitize_html(search_result.get('title'))),
                    'contents': sanitize_html(search_result.get('contents')),
                    'content_plain_text': await request_post_content(search_result.get('postUrl')),
                    'thumbnails': [thumbnail.get('url') for thumbnail in search_result.get('thumbnails')],
                    'target_keyword': target_keyword,
                    'channel_keyname': 'naver-blog'
                }
        await send(producer, 'scraping', post)
        post_list.append(post)
    await producer.stop()
    return post_list


async def request_post_content(url: str):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        response_string = await response.text()
        soup = bs(response_string, "html.parser")
        frame = soup.find('iframe', id='mainFrame')
        frame_addr = 'https://blog.naver.com/' + frame['src']

    async with aiohttp.ClientSession() as session:
        response = await session.get(frame_addr)
        response_string = await response.text()
        soup = bs(response_string, "lxml") 

    if soup.find("div", attrs={"class":"se-main-container"}):
        text = soup.find("div", attrs={"class":"se-main-container"}).get_text()
        text = text.replace("\n","") #공백 제거
        return text
    return None
