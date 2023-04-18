from dto import *
from fastapi import FastAPI
from kafka_producer import *
from scraping.fiddler.scraping_naver_blog import extract_information_from_search_results
from scraping.fiddler.scraping_naver_blog import request_post_list as naver_blog
from scraping.fiddler.scraping_bigkinds import request_news_list as bigkinds
# from scraping.fiddler.scraping_naver_news import request_news_list as naver_news

app = FastAPI()


@app.post('/scraping_naver_blog', response_model=List[NaverBlogResponse])
async def request_naver_blog(params: NaverBlogRequestParams):
    posts = list()
    producer = await initialize_producer()
    await producer.start()

    async def extend_posts(current_page: int):
        posts_per_page = await naver_blog(
                producer=producer,
                target_keyword=params.target_keyword,
                start_date=params.start_date,
                end_date=params.end_date,
                current_page=current_page
            )
        posts.extend(posts_per_page)

    total_count, _ = await extract_information_from_search_results(
        target_keyword=params.target_keyword,
        start_date=params.start_date,
        end_date=params.end_date,
        current_page=1
    )

    current_page = 1
    while True:
        if len(posts) > total_count:
            break
        if params.page_limit is not None and current_page > params.page_limit:
            break
        await extend_posts(current_page=current_page)
        current_page += 1
    await producer.stop()
    return posts


@app.post('/scraping_bigkinds', response_model=List[BigkindsResponse])
async def request_bigkinds(params: BigkindsRequestParams):
    return await bigkinds(
        target_keyword=params.target_keyword,
        start_date=params.start_date,
        end_date=params.end_date,
        limit=params.limit
    )


# @app.post('/scraping_naver_news', response_model=List[NaverNewsResponse])
# async def request_naver_news(params: NaverNewsResponseParams):
#     return await naver_news(
#         target_keyword=params.target_keyword
#     )
