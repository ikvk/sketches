import re
import requests
import urllib.parse


def valeri():
    with open('page_data.txt', 'r', encoding='utf-8') as f:
        raw = f.read()

    # load
    for i in [str(i.group()) for i in re.finditer('/mp3/.+?\.mp3', raw)]:
        url = 'https://inkompmusic.ru{}'.format(i)
        name = urllib.parse.unquote(url.split('/')[-1].replace('+', ' ').replace('_(Inkompmusic.ru)', ''))
        print(name)
        data = requests.get(url.format(i)).content
        with open('valeri/{}'.format(name), 'wb') as handler:
            handler.write(data)
