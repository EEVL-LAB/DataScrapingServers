import os
import redis


def redis_connection() -> redis.StrictRedis:
    return redis.StrictRedis(
        host=os.environ["REDIS_HOST"],
        port=os.environ["REDIS_PORT"],
        db=os.environ["REDIS_DB_NUM"]
    )
    

conn: redis.StrictRedis = redis_connection()