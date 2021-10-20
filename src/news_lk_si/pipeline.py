import os
from bs4 import BeautifulSoup
from utils import www
from news_lk_si._utils import log
from news_lk_si.scrape import scrape, get_name_base
from news_lk_si.extract import extract
from news_lk_si.text_to_audio import text_to_audio

MIN_N_URL = 240

def is_processed(url):
    name_base = get_name_base(url)

    url_remote_audio = os.path.join(
        'https://raw.githubusercontent.com/nuuuwan',
        'news_lk_si/data',
        f'{name_base}.html',
    )
    return www.exists(url_remote_audio)


def get_urls():
    BASE_URL = 'https://www.dinamina.lk/editorial'
    html = www.read(BASE_URL)
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for a in soup.find_all('a'):
        href = a['href']
        if 'http' not in href and len(href) > MIN_N_URL:
            url = 'https://www.dinamina.lk' + href
            urls.append(url)
    return urls


def process(url):
    html_file = scrape(url)
    md_file = extract(html_file)
    if md_file:
        text_to_audio(md_file)


def process_all():
    urls = get_urls()
    n = len(urls)
    for i, url in enumerate(urls):
        i1 = i + 1
        log.info(f'Processing {i1}/{n} "{url}"...')
        if is_processed(url):
            log.warning(f'{url} already processed. Aborting process')
        else:
            process(url)


if __name__ == '__main__':
    process_all()
