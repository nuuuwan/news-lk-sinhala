from bs4 import BeautifulSoup
from utils import www, hashx
from news-lk-sinhala import _utils

TEST_URL = 'https://www.dinamina.lk/2021/10/20/%E0%B6%9A%E0%B6%AD%E0%B7%94%E0%B7%80%E0%B7%90%E0%B6%9A%E0%B7%92%E0%B6%BA/132810/%E0%B6%91%E0%B6%B1%E0%B7%8A%E0%B6%B1%E0%B6%AD%E0%B7%8A%E0%B6%9A%E0%B6%BB%E0%B6%AB%E0%B6%BA%E0%B7%99%E0%B6%B1%E0%B7%8A-%E0%B7%83%E0%B7%8F%E0%B6%BB%E0%B7%8A%E0%B6%AE%E0%B6%9A%E0%B6%B8-%E0%B6%BB%E0%B6%A7%E0%B7%80%E0%B6%BD%E0%B7%8A-%E0%B6%AF%E0%B7%84%E0%B6%BA-%E0%B6%85%E0%B6%AD%E0%B6%BB%E0%B6%A7'

def scrape(url):
    h = hashx(url)
    html = www.read(url)
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = []
    for div in soup.find_all('div', class_='field-item even'):
        for p  in div.find_all('p'):
            paragraphs.append(p.text)
    text_file = f'{h}.txt'
    text = '\n\n'.join(paragraphs)
    filex.write(text_file, text)
    n_text = len(text)
    log.info('Wrote {n_text}KB to {text_file}')

if __name__ == '__main__':
    scrape(TEST_URL)
