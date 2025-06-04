from bs4 import BeautifulSoup
import requests
import tldextract


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


def extract_domain_name(bookmark_url):
    extract_result = tldextract.extract(str(bookmark_url))
    domain_name = extract_result.domain
    capitalized_domain_name = domain_name.capitalize()
    
    return capitalized_domain_name


def find_specific_bookmarks_by_search_string(search_str, bookmarks):
    found_bookmarks = [bookmark for bookmark in bookmarks if search_str in bookmark.title or search_str in str(bookmark.url)]

    return found_bookmarks


def find_specific_bookmarks_by_tag_name(tag_name, all_bookmarks):
    found_bookmarks = [bookmark for bookmark in all_bookmarks if tag_name in bookmark.tags]

    return found_bookmarks
