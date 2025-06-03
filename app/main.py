from fastapi import FastAPI

from app.models import Bookmark
from app.utils import extract_domain_name, find_specific_bookmarks, get_page_title_content
from app.database import all_bookmarks


app = FastAPI()


@app.get('/bookmarks/')
def get_bookmarks(search: str | None = None):
    if not search:
        return [{'id': idx + 1, 'title': bookmark.title, 'url': str(bookmark.url)} for idx, bookmark in enumerate(all_bookmarks)]
    
    bookmarks = find_specific_bookmarks(search, all_bookmarks)

    search_result = None
    if bookmarks:
        search_result = [{'title': bookmark.title, 'url': str(bookmark.url)} for bookmark in bookmarks]
    else:
        search_result = {'message': 'No bookmarks found'}

    return search_result


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
