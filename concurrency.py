from urllib import request
import time


def _timeit(fn):
    t = time.time()
    fn()
    print('time:', time.time() - t)


def _sync_request_url(url: str) -> bool:
    wb_data = request.urlopen(url)
    if wb_data.code == 200:
        try:
            print(time.time(), url, len(wb_data.read()))
        except IOError:
            return False
        return True
    else:
        return False


URL_SET = ['https://duckduckgo.com/?q={}'.format(i) for i in range(30)]
statistic_30_urls = """
host: 4 cores 3.4Ghz, 16Gb ram, 11.09 МБайт/с IN, 4.10 МБайт/с OUT

proc_pool
10 = 2.25 sec
5 = 3.08 sec
1 = 13.7 sec

thread_pool
10 = 1.63 sec
5 = 2.92 sec
1 = 13.03 sec

aio_loop
3.72 sec
"""

def proc_pool():
    from multiprocessing import Pool
    with Pool(1) as p:
        res = p.map(_sync_request_url, URL_SET)
        print(len(res), 'ok')


def thread_pool():
    from multiprocessing.pool import ThreadPool
    with ThreadPool(1) as p:
        res = p.map(_sync_request_url, URL_SET)
        print(len(res), 'ok')


def aio_loop():
    import aiohttp
    import asyncio
    async def main():
        async with aiohttp.ClientSession() as session:
            for url in URL_SET:
                async with session.get(url) as response:
                    # print("Status:", response.status)
                    # print("Content-type:", response.headers['content-type'])
                    html = await response.text()
                    # print("Body:", html[:15], "...")
                    print(time.time(), url, len(html))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == '__main__':
    _timeit(
        aio_loop
    )
