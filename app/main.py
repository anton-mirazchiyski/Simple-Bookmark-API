from bs4 import BeautifulSoup
from fastapi import FastAPI
import requests

from app.models import Bookmark


app = FastAPI()


def get_page_title_content(bookmark_url):
    title_content = ''

    try:
        response = requests.get(bookmark_url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title_element = soup.find('head').find('title')
        if title_element is not None:
            title_content = title_element.text
    except:
        return
    
    return title_content


@app.post('/bookmarks/')
def create_bookmark(bookmark: Bookmark):
    if bookmark.title is None:
        page_title_content = get_page_title_content(bookmark.url)
        if page_title_content:
            bookmark.title = page_title_content

    return bookmark
