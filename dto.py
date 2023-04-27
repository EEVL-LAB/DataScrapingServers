from typing import List
from pydantic import BaseModel


class NaverBlogRequestParams(BaseModel):
    target_keyword: str
    start_date: str = '2022-01-01'
    end_date: str = '2023-01-01'
    page_limit: int = None



class BigkindsRequestParams(BaseModel):
    target_keyword: str
    start_date: str = '2022-01-01'
    end_date: str = '2023-01-01'
    limit: int = 24
