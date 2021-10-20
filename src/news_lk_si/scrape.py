from utils import filex, hashx, www
from news_lk_si._utils import log

LANG = 'si'
N_HASH = 8
NEWS_PAPER_NAME = 'dinamina'


def get_name_base(url):
    h = hashx.md5(url)[:N_HASH]
    date_str = url[24:34]
    date_id = date_str.replace('/', '_')
    return f'news_lk_si.{date_id}.{NEWS_PAPER_NAME}.{h}'


def scrape(url):
    html = www.read(url)
    name_base = get_name_base(url)
    html_file = f'/tmp/{name_base}.html'
    filex.write(html_file, html)
    log.info(f'Wrote {html_file}')
    return html_file
