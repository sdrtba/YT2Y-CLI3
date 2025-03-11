import logging
from yt_dlp import YoutubeDL
import os
from transfer import upload

LOG_FILE = 'etc/download.log'
ARCHIVE_FILE = 'etc/archive.txt'
COOKIE_FILE = 'etc/cookies'
OUTPUT_DIR = 'output'

def hook(d: dict) -> None:
    if d['status'] == 'finished':
        song_title = d.get('info_dict', {}).get('title', None)
        if song_title:
            with open('etc/songs.txt', 'a', encoding='utf-8') as ds_f:
                ds_f.write(song_title + '\n')
            upload(song_title)

def download() -> None:
    url1 = 'https://www.youtube.com/playlist?list=PLcLWzrwuuZhP-qE-ttdWn0x8ANgR8xzpC'
    url2 = 'https://www.youtube.com/watch?v=H6tNm72cMA8'
    url3 = 'https://www.youtube.com/watch?v=_xjp42aZ8iI'
    url = input('Enter url: ') or url1

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            pass

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )

    ydl_opts = {
        'logger': logging.getLogger(__name__),
        'outtmpl': '%(title)s.%(ext)s',
        'paths': {'home': OUTPUT_DIR},
        'format': 'ba[ext=m4a]',
        'retries': 4,
        'quiet': False,
        'progress_hooks': [hook],
        'skip_unavailable_fragments': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'download_archive': ARCHIVE_FILE,
        'cookiefile': COOKIE_FILE
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    download()
