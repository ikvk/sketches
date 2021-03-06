"""
Поиск файлов с похожими именами
"""
import os, re

IGNORED_NAMES = ('back', 'cd', 'front', 'inside')
IGNORED_EXTENSIONS = ('txt', 'log', 'jpg', 'jpeg', 'png', 'cue', '', 'm3u')
PATH = 'D:\Музыка\Гитара\Tommy Emmanuel'


def duplicate_files():
    res = {}
    file_cnt = 0
    for root, subdirs, files in os.walk(PATH):
        for file_name in files:
            clear_file_name = re.sub("[^a-zA-Z ]+", "", file_name.rsplit('.', 1)[0]).lower()
            if clear_file_name in IGNORED_NAMES:
                continue
            file_ext = file_name.split('.')[-1].replace('.', '').lower()
            if file_ext in IGNORED_EXTENSIONS:
                continue
            words = tuple(i.strip() for i in clear_file_name.split(' ') if bool(i) and len(i) > 1)
            # print(' - ', words)
            res.setdefault(words, []).append(os.path.join(root, file_name))
            file_cnt += 1

    for key in sorted(res.keys(), key=lambda x: len(res[x])):
        print(key, len(res[key]))
        for path in res[key]:
            print(' - {}'.format(path))
            pass

    print()
    print('total: {}'.format(file_cnt))
    print('uniq: {}'.format(len(res)))


duplicate_files()
