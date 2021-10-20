import os
from bs4 import BeautifulSoup
from utils import filex
from news_lk_si._utils import log


MIN_N_PARAGRAPHS = 2
MIN_N_PARAGRAPH = 5


def extract(html_file):
    name_base = html_file[5:-5]
    md_file = f'/tmp/{name_base}.md'

    html = filex.read(html_file)
    soup = BeautifulSoup(html, 'html.parser')

    paragraphs = []

    h1_title = soup.find('h1', class_='title')
    paragraphs.append('# ' + h1_title.text)

    for div in soup.find_all('div', class_='field-item even'):
        for p in div.find_all('p'):
            paragraph = p.text
            if len(paragraph) >= MIN_N_PARAGRAPH:
                paragraphs.append(paragraph)

    if len(paragraphs) >= MIN_N_PARAGRAPHS:
        text = '\n\n'.join(paragraphs)
        filex.write(md_file, text)
        log.info(f'Wrote {md_file}')
        return md_file
    else:
        log.warn(f'{html_file} is too short. Not extracting.')
        return None
