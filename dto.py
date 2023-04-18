from typing import List
from pydantic import BaseModel


class NaverBlogRequestParams(BaseModel):
    target_keyword: str
    start_date: str = '2022-01-01'
    end_date: str = '2023-01-01'
    page_limit: int = None


class NaverBlogResponse(BaseModel):
    url: str
    title: str
    contents: str
    content_plain_text: str
    thumbnails: List[str]
    target_keyword: str
    channel_keyname: str


class BigkindsRequestParams(BaseModel):
    target_keyword: str
    start_date: str = '2022-01-01'
    end_date: str = '2023-01-01'
    limit: int = 24


class BigkindsResponse(BaseModel):
    url: str
    title: str
    contents: str
    content_plain_text: str
    thumbnails: List[str]
    target_keyword: str
    channel_keyname: str
    
    
# class NaverNewsResponseParams(BaseModel):
#     target_keyword: str


# class NaverNewsResponse(BaseModel):
#     url: str
#     title: str
#     contents: str
#     content_plain_text: str
#     thumbnails: List[str]
#     target_keyword: str
#     channel_keyname: str
