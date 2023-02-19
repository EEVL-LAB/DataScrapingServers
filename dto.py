from pydantic import BaseModel


class NaverBlogRequestParams(BaseModel):
    target_keyword: str
    page_limit: int = 1


class NaverNewsResponseParams(BaseModel):
    target_keyword: str


class BigkindsRequestParams(BaseModel):
    start_date: str = '2022-01-01'
    end_date: str = '2023-01-01'
    limit: int = 24
