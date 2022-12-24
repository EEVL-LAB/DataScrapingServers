import json
import requests
from urllib import parse


def request_search_list(target_keyword: str=None) -> list:
    encoded_keyword = parse.quote(target_keyword)
    url = f'https://section.blog.naver.com/ajax/SearchList.naver?countPerPage=7&currentPage=1&endDate=&keyword={encoded_keyword}&orderBy=sim&startDate=&type=post'
    headers = {
        "Host":"section.blog.naver.com",
        "Connection":"keep-alive",
        "Accept":"application/json, text/plain, */*",
        "Referer":f'https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword={encoded_keyword}',
        # "Cookie":"NNB=HMNW2RUCK6TGG; JSESSIONID=8639AE8F5E00F8E7D608FED7D9A33445.jvm1"
    }
    response = requests.get(
        url=url,
        headers=headers
    )
    response_string = response.content.decode('utf-8')
    response_string = response_string.split('\n')[1]
    response_dict = json.loads(response_string)
    return response_dict.get('result').get('searchList')


if __name__ == "__main__":
    search_list = request_search_list('삼쩜삼')
    for search in search_list:
        print(json.dumps(search, indent=4, ensure_ascii=False))
        print('\n\n', '*'*1000, '\n\n')
        break
