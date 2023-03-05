from typing import List
from pydantic import BaseModel


class NaverBlogRequestParams(BaseModel):
    target_keyword: str
    page_limit: int = 1

class NaverBlogResponse(BaseModel):
    url: str
    title: str
    contents: str
    content_plain_text: str
    thumbnails: List[str]


class NaverNewsResponseParams(BaseModel):
    target_keyword: str


class NaverNewsResponse(BaseModel):
    url: str
    title: str
    contents: str
    content_plain_text: str
    thumbnails: List[str]


class BigkindsRequestParams(BaseModel):
    start_date: str = '2022-01-01'
    end_date: str = '2023-01-01'
    limit: int = 24


class BigkindsResponse(BaseModel):
    url: str
    title: str
    contents: str
    content_plain_text: str
    thumbnails: List[str]