import os
import redis
import aiohttp
import asyncio


conn = redis.StrictRedis(
    host=os.environ["REDIS_HOST"],
    port=os.environ["REDIS_PORT"],
    db=os.environ["REDIS_DB_NUM"]
)


async def get_params_for_naver_blog():
    pass


async def get_params_for_bigkinds():
    pass


async def request_scraping_naver_blog():
    while True:
        pass


async def request_scarping_bigkinds():
    while True:
        pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_soon()
    loop.call_soon()
    loop.run_forever()
    loop.close()