from dto import *
from fastapi import FastAPI
from scraping.fiddler.scraping_naver_blog import request_post_list as naver_blog
# from scraping.fiddler.scraping_naver_news import request_news_list as naver_news
from scraping.fiddler.scraping_bigkinds import request_news_list as bigkinds


app = FastAPI()


@app.post('/scraping_naver_blog', response_model=List[NaverBlogResponse])
async def request_naver_blog(params: NaverBlogRequestParams):
    posts = list()

    async def extend_posts(current_page: int):
        posts_per_page = await naver_blog(
                target_keyword=params.target_keyword,
                start_date=params.start_date,
                end_date=params.end_date,
                current_page=current_page
            )
        posts.extend(posts_per_page)

    if params.page_limit is not None:
        for current_page in range(1, params.page_limit+1):
            await extend_posts(current_page=current_page)
            print(f'[{current_page} page complete]')
        return posts

    current_page = 1
    while True:
        try:
            await extend_posts(current_page=current_page)
            print(f'[{current_page} page complete]')
            current_page += 1
        except:
            return posts


# @app.post('/scraping_naver_news', response_model=List[NaverNewsResponse])
# async def request_naver_news(params: NaverNewsResponseParams):
#     return await naver_news(
#         target_keyword=params.target_keyword
#     )


@app.post('/scraping_bigkinds', response_model=List[BigkindsResponse])
async def request_bigkinds(params: BigkindsRequestParams):
    return await bigkinds(
        target_keyword=params.target_keyword,
        start_date=params.start_date,
        end_date=params.end_date,
        limit=params.limit
    )
