from urllib import request
import time

"""
16 cores, 24 logic cores

30 urls:
    sync_req        : 8.27 sec
    proc_pool 10    : 1.12 sec
    thread_pool 10  : 1.11 sec
    aio_loop_sync   : 3.62 sec
    aio_loop_gather : 0.47 sec

100 urls:
    sync_req        : 31.57 sec
    proc_pool 20    :  1.81 sec
    thread_pool 20  :  2.00 sec
    aio_loop_sync   : 11.01 sec
    aio_loop_gather :  0.65 sec
    
500 urls:
    proc_pool 30    :  7.56 sec
    thread_pool 30  :  7.77 sec
    aio_loop_sync   : 47.31 sec
    aio_loop_gather :  0.96 sec
"""

URL_SET = ['https://ya.ru/?q={}'.format(i) for i in range(500)]  # https://duckduckgo.com/?q={}


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


def sync_req():
    for url in URL_SET:
        print(_sync_request_url(url))


def proc_pool():
    from multiprocessing import Pool
    with Pool(20) as p:
        res = p.map(_sync_request_url, URL_SET)
        print(len(res), 'ok')


def thread_pool():
    from multiprocessing.pool import ThreadPool
    with ThreadPool(20) as p:
        res = p.map(_sync_request_url, URL_SET)
        print(len(res), 'ok')


def aio_loop_sync():
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


def aio_loop_gather():
    import asyncio
    import aiohttp
    import time

    async def fetch_url(session, url):
        async with session.get(url) as response:
            html = await response.text()
            print(f"{time.time():.2f} | {url} | {len(html)} bytes")

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(session, url) for url in URL_SET]
            await asyncio.gather(*tasks)  # *параллельное выполнение

    asyncio.run(main())  # Современный способ запуска


if __name__ == '__main__':
    _timeit(
        aio_loop_gather
    )
