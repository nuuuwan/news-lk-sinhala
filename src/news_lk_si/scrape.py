import os

from bs4 import BeautifulSoup
from gtts import gTTS
from pydub import AudioSegment
from utils import filex, hashx, www

from news_lk_si._utils import log

LANG = 'si'
N_HASH = 8
MIN_N_PARAGRAPH = 5
NEWS_PAPER_NAME = 'dinamina'

# https://github.com/nuuuwan/news_lk_si/blob/data/news_lk_si.f481e69b.mp3


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def get_name_base(url):
    h = hashx.md5(url)[:N_HASH]
    date_str = url[24:34]
    date_id = date_str.replace('/', '')
    return f'news_lk_si.{NEWS_PAPER_NAME}.{date_id}.{h}'


def scrape(url):
    name_base = get_name_base(url)
    text_file = f'/tmp/{name_base}.md'

    if os.path.exists(text_file):
        log.warning(f'{text_file} exists. Aborting scrape.')
    else:
        html = www.read(url)
        soup = BeautifulSoup(html, 'html.parser')

        paragraphs = []

        h1_title = soup.find('h1', class_='title')
        paragraphs.append('# ' + h1_title.text)

        for div in soup.find_all('div', class_='field-item even'):
            for p in div.find_all('p'):
                paragraph = p.text
                if len(paragraph) >= MIN_N_PARAGRAPH:
                    paragraphs.append(paragraph)
        text = '\n\n'.join(paragraphs)

        filex.write(text_file, text)
        n_text_k = len(text) / 1_000.0
        log.info(f'Scraped "{url}" ({n_text_k:.0f}KB) to {text_file}')

    return text_file


def text_to_audio(text_file):
    paragraphs = filex.read(text_file).split('\n\n')
    file_base = text_file[:-4]
    combined_audio_file = f'{file_base}.mp3'

    if os.path.exists(combined_audio_file):
        log.warning(f'{combined_audio_file} exists. Aborting TTS.')

    else:
        tmp_base = file_base[5:]

        n = len(paragraphs)
        audio_files = []
        for i, paragraph in enumerate(paragraphs):
            i1 = i + 1
            audio_file = f'/tmp/tmp_{tmp_base}.{i1:03d}.mp3'
            if os.path.exists(audio_file):
                log.warning(f'{audio_file} exists. Aborting TTS.')
            else:
                text = paragraph.replace('# ', '')
                try:
                    tts = gTTS(text, lang=LANG)
                    tts.save(audio_file)
                    log.info(f'Wrote {i1}/{n} to {audio_file}')
                except:
                    continue
            audio_files.append(audio_file)

        combined_audio = None
        for audio_file in audio_files:
            audio = AudioSegment.from_file(audio_file)

            if combined_audio is None:
                combined_audio = audio
            else:
                combined_audio += audio
        combined_audio.export(combined_audio_file)
        log.info(f'Wrote combined audio to {combined_audio_file}')
    return combined_audio_file


def get_urls():
    BASE_URL = 'https://www.dinamina.lk/editorial'
    html = www.read(BASE_URL)
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for a in soup.find_all('a'):
        href = a['href']
        if 'http' not in href and len(href) > 240:
            url = 'https://www.dinamina.lk' + href
            urls.append(url)
    return urls


def process(url):
    text_file = scrape(url)
    text_to_audio(text_file)


def is_alread_parsed(url):
    name_base = get_name_base(url)

    url_remote_audio = os.path.join(
        'https://raw.githubusercontent.com/nuuuwan',
        'news_lk_si/data',
        f'{name_base}.md',
    )
    return www.exists(url_remote_audio)


def process_all():
    urls = get_urls()
    n = len(urls)
    for i, url in enumerate(urls):
        i1 = i + 1
        log.info(f'Processing {i1}/{n} "{url}"...')
        if is_alread_parsed(url):
            log.warning(f'{url} already processed. Aboring process')
        else:
            process(url)


if __name__ == '__main__':
    process_all()
