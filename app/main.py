from fastapi import FastAPI

from app.models import Bookmark
from app.utils import extract_domain_name, get_page_title_content


app = FastAPI()

all_bookmarks = []


@app.get('/bookmarks/')
def get_all_bookmarks():
    return [{'id': idx + 1, 'title': bookmark.title, 'url': str(bookmark.url)} for idx, bookmark in enumerate(all_bookmarks)]


@app.post('/bookmarks/')
def create_bookmark(bookmark: Bookmark):
    if bookmark.title is None:
        page_title_content = get_page_title_content(bookmark.url)
        if page_title_content:
            bookmark.title = page_title_content
        else:
            domain_name = extract_domain_name(bookmark.url)
            bookmark.title = domain_name
    
    all_bookmarks.append(bookmark)

    return bookmark
