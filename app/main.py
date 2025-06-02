from fastapi import FastAPI

from app.models import Bookmark
from app.utils import get_page_title_content


app = FastAPI()


@app.post('/bookmarks/')
def create_bookmark(bookmark: Bookmark):
    if bookmark.title is None:
        page_title_content = get_page_title_content(bookmark.url)
        if page_title_content:
            bookmark.title = page_title_content

    return bookmark
