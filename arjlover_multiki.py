"""
grab http://multiki.arjlover.net
just set SAVE_PATH var and run
"""
import shutil
import requests

SAVE_PATH = 'E:/Мультфильмы/Советские'


def download_file(url: str, file_path: str):
    with requests.get(url, stream=True) as r:
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def main(raw: str):
    for bi, block in enumerate(raw.split('</tr>')):
        # names
        name, link, ext = '', '', ''
        for i, r in enumerate(block.split('</td>')):
            if i == 1:
                bad_chars = ['/', '\\', ':', '*', '?', '"', '>', '<', '|', ]
                name = ''.join(c for c in r.split('>')[-2].replace('</a', '') if c not in bad_chars)
            elif i == 5:
                link = 'http://multiki.arjlover.net' + \
                       r.split('onClick')[0].replace('<td><a href="', '').replace('"', '').strip()
                ext = link.split('.')[-1]
        if not name:
            continue
        print(name, ext, link, '{}/3655'.format(bi, ))
        # if bi < 32:  # 32big 36small continue
        # download
        err = ''
        try:
            download_file(link, '{}/{}.{}'.format(SAVE_PATH, name, ext))
        except Exception as e:
            err = str(e)
            print(err)
        # log
        with open('{}/_log.txt'.format(SAVE_PATH), 'a') as log_file:
            log_line = '{} # {}\n'.format(name, link)
            if err:
                log_file.write('ERR: {} # {}'.format(err, log_line))
            else:
                log_file.write(log_line)


if __name__ == '__main__':
    with open('files/arjlover_multiki.txt', 'r', encoding='utf8') as f:
        raw_data = f.read()
    main(raw_data)
