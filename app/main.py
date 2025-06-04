from fastapi import FastAPI

from app.models import Bookmark
from app.utils import extract_domain_name, find_specific_bookmarks_by_search_string, find_specific_bookmarks_by_tag_name, get_page_title_content
from app.database import all_bookmarks


app = FastAPI()


@app.get('/bookmarks/')
def get_bookmarks(tag: str | None = None, search: str | None = None):
    if not search and not tag:
        return [{'id': idx + 1, 'title': bookmark.title, 'url': str(bookmark.url)} for idx, bookmark in enumerate(all_bookmarks)]
    
    specific_bookmarks = None

    if tag:
        specific_bookmarks = find_specific_bookmarks_by_tag_name(tag, all_bookmarks)
        if search is not None:
            specific_bookmarks = find_specific_bookmarks_by_search_string(search, specific_bookmarks)
    elif search:
        specific_bookmarks = find_specific_bookmarks_by_search_string(search, all_bookmarks)

    if specific_bookmarks:
        return [{'title': bookmark.title, 'url': str(bookmark.url)} for bookmark in specific_bookmarks]

    return {'message': 'No bookmarks found'}


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
