import requests

url = 'https://github.com/ikvk/imap_tools/issues/{}'
for i in range(0, 200):
    resp = requests.get(url.format(i))
    if resp.status_code == 404:
        continue
    print(i)

    with open('C:\kvk\Загрузки\imap_tools_issues/{}.html'.format(i), 'wb') as handler:
        handler.write(resp.content)

