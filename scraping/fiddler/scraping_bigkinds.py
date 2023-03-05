import aiohttp
import asyncio


available_keys = [
    'TITLE',
    'DATE',
    'CONTENT',
    'IMAGE_URL'
]


async def request_news_list(start_date: str, end_date: str, limit: int):
    url = f'https://www.bigkinds.or.kr/news/subMainData.do?pageInfo=mainNews&login_chk=&LOGIN_SN=&LOGIN_NAME=&indexName=news&keyword=&byLine=&searchScope=1&searchFtr=3&startDate={start_date}&endDate={end_date}&sortMethod=date&contentLength=100&providerCode=&categoryCode=&incidentCode=&dateCode=&highlighting=false&sessionUSID=&sessionUUID=test&listMode=&categoryTab=&newsId=&delnewsId=&delquotationId=&delquotationtxt=&filterProviderCode=&filterCategoryCode=&filterIncidentCode=&filterDateCode=&filterAnalysisCode=&startNo=1&resultNumber={limit}&topmenuoff=&resultState=newsSubMain&keywordJson=&keywordFilterJson=&realKeyword=&keywordYn=Y&totalCount=&interval=&quotationKeyword1=&quotationKeyword2=&quotationKeyword3=&printingPage=&searchFromUseYN=N&searchFormName=&searchFormSaveSn=&mainTodayPersonYn=&period=&sectionDiv='
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
        for response in responses:
            result.append(
                {
                    'url': '',
                    'title': response.get('TITLE'),
                    'contents': response.get('CONTENT'),
                    'content_plain_text': response.get('CONTENT').replace('\n', ' '),
                    'thumbnails': [response.get('IMAGE_URL')],
                }
            )
        return result
