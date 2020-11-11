def masha():
    import requests

    url = 'http://skazkiwsem.ru/Malysham/masha-i-oyka/files/mobile/{}.jpg'
    for i in range(1, 97):
        print(i)
        img_data = requests.get(url.format(i)).content
        with open('m/{}.jpg'.format(i), 'wb') as handler:
            handler.write(img_data)


