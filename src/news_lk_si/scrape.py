import os

from bs4 import BeautifulSoup
from gtts import gTTS
from pydub import AudioSegment
from utils import filex, hashx, www

from news_lk_si._utils import log

LANG = 'si'
N_HASH = 8


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def scrape(url):
    h = hashx.md5(url)[:N_HASH]
    text_file = f'/tmp/news_lk_si.{h}.txt'

    if os.path.exists(text_file):
        log.warning(f'{text_file} exists. Aborting scrape.')
    else:
        html = www.read(url)
        soup = BeautifulSoup(html, 'html.parser')

        paragraphs = []

        h1_title = soup.find('h1', class_='title')
        paragraphs.append(h1_title.text)

        for div in soup.find_all('div', class_='field-item even'):
            for p in div.find_all('p'):
                paragraphs.append(p.text)
        text = '\n\n'.join(paragraphs)

        filex.write(text_file, text)
        n_text_k = len(text) / 1_000.0
        log.info(f'Scraped "{url}" ({n_text_k:.0f}KB) to {text_file}')

    return text_file


def text_to_audio(text_file):
    paragraphs = filex.read(text_file).split('\n\n')
    file_base = text_file[:-4]
    tmp_base = file_base[5:]

    n = len(paragraphs)
    audio_files = []
    for i, paragraph in enumerate(paragraphs):
        if len(paragraph) == 0:
            continue
        i1 = i + 1
        audio_file = f'/tmp/tmp_{tmp_base}.{i1:03d}.mp3'
        if os.path.exists(audio_file):
            log.warning(f'{audio_file} exists. Aborting TTS.')
        else:
            tts = gTTS(paragraph, lang=LANG)
            tts.save(audio_file)
            log.info(f'Wrote {i1}/{n} to {audio_file}')
        audio_files.append(audio_file)

    combined_audio = None
    for audio_file in audio_files:
        audio = AudioSegment.from_file(audio_file)

        if combined_audio is None:
            combined_audio = audio
        else:
            combined_audio += audio
    combined_audio_file = f'{file_base}.mp3'
    combined_audio.export(combined_audio_file)
    log.info(f'Wrote combined audio to {combined_audio_file}')


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
    log.info(f'Processing "{url}"...')
    text_file = scrape(url)
    text_to_audio(text_file)


def process_all():
    for url in get_urls():
        process(url)
        break


if __name__ == '__main__':
    process_all()
