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


def masha():
    import requests

    url = 'http://skazkiwsem.ru/Malysham/masha-i-oyka/files/mobile/{}.jpg'
    for i in range(1, 97):
        print(i)
        img_data = requests.get(url.format(i)).content
        with open('m/{}.jpg'.format(i), 'wb') as handler:
            handler.write(img_data)

# todo http://multiki.arjlover.net/multiki/

# todo https://torgi.gov.ru
