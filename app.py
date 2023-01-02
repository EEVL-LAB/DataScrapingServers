from dto import *
from fastapi import FastAPI
from scraping.fiddler.scraping_naver_blog import request_post_list as naver_blog
from scraping.fiddler.scraping_naver_news import request_news_list as naver_news


app = FastAPI()


@app.post('/scarping_naver_blog')
async def request_naver_blog(params: NaverBlogParams):
    posts = list()

    async def extend_posts(current_page: int):
        posts_per_page = await naver_blog(
                target_keyword=params.target_keyword,
                current_page=current_page
            )
        posts.extend(posts_per_page)

    if params.page_limit is not None:
        for current_page in range(1, params.page_limit+1):
            await extend_posts(current_page=current_page)
        return posts

    current_page = 1
    while True:
        try:
            extend_posts(current_page=current_page)
            current_page += 1
        except:
            return posts
