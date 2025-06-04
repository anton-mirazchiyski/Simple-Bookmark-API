from pydantic import BaseModel, HttpUrl


class Bookmark(BaseModel):
    title : str | None = None
    url : HttpUrl
    tags : set[str] = set()
