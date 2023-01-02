from pydantic import BaseModel


class NaverBlogParams(BaseModel):
    target_keyword: str
    page_limit: int = 1


class NaverNewsParams(BaseModel):
    target_keyword: str