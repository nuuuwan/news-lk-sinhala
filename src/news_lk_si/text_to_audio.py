import os
from gtts import gTTS
from pydub import AudioSegment
from utils import filex
from news_lk_si._utils import log

LANG = 'si'


def text_to_audio(md_file):
    paragraphs = filex.read(md_file).split('\n\n')
    file_base = md_file[:-4]

    tmp_base = file_base[5:]

    n = len(paragraphs)
    audio_files = []
    for i, paragraph in enumerate(paragraphs):
        i1 = i + 1
        audio_file = f'/tmp/tmp_{tmp_base}.{i1:03d}.mp3'
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
    combined_audio_file = f'{file_base}.mp3'
    combined_audio.export(combined_audio_file)
    log.info(f'Wrote combined audio to {combined_audio_file}')
    return combined_audio_file
