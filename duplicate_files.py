import os, re


def file_duplicates():
    res = {}
    file_cnt = 0
    ignored_names = ('back', 'cd', 'front', 'inside',)
    for root, subdirs, files in os.walk('C:/Загрузки/Armik сборники'):
        for file_name in files:
            clear_file_name = re.sub("[^a-zA-Z ]+", "", file_name.rsplit('.', 1)[0]).lower().replace('armik', '')
            if clear_file_name in ignored_names:
                continue
            file_ext = file_name.split('.')[-1].replace('.', '').lower()
            if file_ext in ('txt', 'log', 'jpg', 'jpeg', 'png', 'cue', '',):
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


file_duplicates()


'''
all
total: 90
uniq: 79

'''