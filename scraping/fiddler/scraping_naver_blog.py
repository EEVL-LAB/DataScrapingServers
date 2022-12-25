import json
import asyncio
import aiohttp
from urllib import parse
from utils import sanitize_html


async def request_post_list(target_keyword: str=None) -> list:

    async def request_search_list(target_keyword: str=None) -> str:
        encoded_keyword = parse.quote(target_keyword)
        url = f'https://section.blog.naver.com/ajax/SearchList.naver?countPerPage=7&currentPage=1&endDate=&keyword={encoded_keyword}&orderBy=sim&startDate=&type=post'
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
    for search_result in search_results:
        post_list.append(
            {
                'url': search_result.get('postUrl'),
                'title': search_result.get('noTagTitle', sanitize_html(search_result.get('title'))),
                'contents': sanitize_html(search_result.get('contents')),
                'thumbnails': search_result.get('thumbnails')
            }
        )

    return post_list


if __name__ == "__main__":
    post_list = asyncio.run(
        request_post_list('파스타')
    )
    print(
        json.dumps(
            post_list,
            indent=4,
            ensure_ascii=False
        )
    )
    
