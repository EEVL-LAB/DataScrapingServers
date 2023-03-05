import json
import aiohttp
import asyncio
from urllib import parse
from scraping.fiddler.utils import sanitize_html
from html.parser import HTMLParser
from typing import List, Tuple


class NewsHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.is_news = False
        self._news_list = list()


    @property
    def news_list(self):
        return self._news_list


    def handle_starttag(self, tag: str, attrs: List[Tuple]) -> None:
        if len(attrs) < 2:
            return
        attr_class = attrs[1][1]
        if tag == 'a' and attr_class == 'news_tit':
            attr_dict = dict(attrs)
            self._news_list.append(
                {
                    'url': attr_dict.get('href'),
                    'title': attr_dict.get('title'),
                    'contents': '',
                    'content_plain_text': '',
                    'thumbnails': []
                }
            )
            self.is_news = True


    def handle_endtag(self, tag: str) -> None:
        if tag == 'a':
            self.is_news = False
            


async def request_news_list(target_keyword: str=None) -> list:

    async def request_search_list(target_keyword: str=None):
        encoded_keyword = parse.quote(target_keyword)
        url = f'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={encoded_keyword}'
        headers = {
            "Host":"search.naver.com",
        }
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url=url,
                headers=headers
            )
            response_string = await response.text()
            return response_string

    response_string = await request_search_list(target_keyword=target_keyword)
    parser = NewsHTMLParser()
    parser.feed(response_string)
    return parser.news_list
    
