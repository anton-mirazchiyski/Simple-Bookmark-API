from bs4 import BeautifulSoup
import requests


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
