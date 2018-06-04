# import random
# import requests
# import json
# import asyncio
# import aiohttp
# import time
# import os
# import glob
# import re
#
# from mzitu.constants import (
#     IMAGE_FOLDER_UNIX_LIKE,
#     USER_AGENT_LIST,
#     PROXY_SOURCE_URL,
# )
# from mzitu.runtimes.redis import mzitu_image_queue, mzitu_url_queue
# from mzitu.models import DownloadedSuit
# from mzitu.runtimes.url_parser import (
#     proxy_request,
#     get_max_page_num,
#     get_proxy_url,
#     header,
# )
# from mzitu.runtimes.proxy_ip import GetProxyIp
#
# NUMBERS = range(1, 51)
# URL = 'http://www.mzitu.com/135699'
#
# async def fetch_async(url, proxy):
#     async with aiohttp.request('GET', url, proxy=proxy['https']) as r:
#         data = await r.text()
#     return data
#
#
# def async_get_images_urls(suite_url):
#     """利用asycnio来替换之前的多线程处理"""
#     suit_info = DownloadedSuit.objects.filter(url=suite_url).first()
#
#     re_download = False
#     if suit_info:
#         print("该套牌已在DB中，确认是否存在，确认套图是否完整...")
#         file_name = suit_info.name
#         max_page_num = suit_info.max_page
#         suit_folder = os.path.join(IMAGE_FOLDER_UNIX_LIKE, file_name)
#         item_list = glob.glob('{}/*.jpg'.format(suit_folder))
#         if len(item_list) >= max_page_num:
#             print("已完整下载，跳过")
#             return False
#         else:
#             print("该套图不完整，重新下载")
#             re_download = True
#
#     page = proxy_request(suite_url)
#
#     max_page_num = get_max_page_num(page)
#     print("max_page_num: {}".format(max_page_num))
#     title = re.search(r'class=\"main-title\">(.+?)</', page)
#     title = title.group(1).strip()
#     title = re.sub(r'[/\\:*?"<>|]', '-', title)  # windows 非法文件夹名字符
#     print(title)
#
#     # 所有下载的文件根目录
#     folder = IMAGE_FOLDER_UNIX_LIKE
#     if not os.path.isdir(folder):
#         os.makedirs(folder, exist_ok=True)
#
#     # 具体suit的文件夹
#     folder = os.path.join(folder, title)
#     if not os.path.isdir(folder):
#         os.makedirs(folder, exist_ok=True)
#
#     # 保存下载内容到sqlite
#     if re_download is False:
#         suit_info = DownloadedSuit(
#             name=title,
#             url=suite_url,
#             max_page=max_page_num,
#         )
#         suit_info.save()
#
#     # threads = []
#     # for i in range(1, max_page_num + 1):
#     #     thread = threading.Thread(target=get_one_pic_url, args=(folder, i, suite_url,))
#     #     thread.start()
#     #     threads.append(thread)
#
#     # for t in threads:
#     #     t.join()
#     start = time.time()
#     event_loop = asyncio.get_event_loop()
#     tasks = [async_get_one_pic_url(folder, num, suite_url) for num in NUMBERS]
#     results = event_loop.run_until_complete(asyncio.gather(*tasks))
#     event_loop.close()
#
#     print("Use asyncio+aiohttp cost: {}".format(time.time() - start))
#
#     return
#
#
# async def async_proxy_request(url):
#     flag = True
#     page = None
#     get_proxy_ip = GetProxyIp(PROXY_SOURCE_URL, random.choice(USER_AGENT_LIST))
#
#     while flag:
#         ip, port = get_proxy_ip.get_random_ip()
#         try:
#             time.sleep(0.5)
#             proxy_url = get_proxy_url(ip, port)
#             proxies = {"https": proxy_url}
#             # proxies = {"http": proxy_url, "https": proxy_url}
#             # response = requests.get(url, proxies=proxies)
#             response = await fetch_async(url, proxies)
#         except Exception as e:
#             print(e)
#             get_proxy_ip.mark_invalid_proxy_ip(ip, port)
#         else:
#             flag = False
#             page = response
#
#     return page
#
#
# async def async_get_one_pic_url(folder, i, suite_url):
#     """分析一个图片的url，并放入redis队列"""
#     sema = asyncio.Semaphore(3)
#     with (await sema):
#         filename = os.path.join(folder, "{:0>2d}.jpg".format(i))
#
#         if os.path.isfile(filename):
#             print("已存在：{}".format(filename))
#             return
#
#         time.sleep(0.5)
#         url = suite_url + '/{}'.format(i)
#         page = await async_proxy_request(url)
#
#         img_url = re.search(r'class=\"main-image(.+?)src=\"(.+?)\"', page)
#         img_url = img_url.groups()[1]
#         print(img_url)
#
#         mzitu_image_queue.put(json.dumps({'filename': filename, 'url': img_url, 'header_url': url}))
#
#     return
#
#
# def requests_get(url, headers=None):
#     get_proxy_ip = GetProxyIp(PROXY_SOURCE_URL, random.choice(USER_AGENT_LIST))
#
#     ip, port = get_proxy_ip.get_random_ip()
#     proxy_url = get_proxy_url(ip, port)
#     proxies = {"https": proxy_url}
#
#     return requests.get(url, headers=headers, proxies=proxies)
#
#
# def download_images_to_local():
#
#     while not mzitu_image_queue.empty():
#         item = mzitu_image_queue.get()
#         item = json.loads(item)
#
#         if os.path.isfile(item['filename']):
#             print("已存在：{}".format(item['filename']))
#             continue
#
#         img_bytes = requests_get(item['url'], headers=header(item['header_url']))
#         with open(item['filename'], 'wb') as f:
#             f.write(img_bytes.content)
#         print("Downloaded {}".format(item['url']))
#         time.sleep(1)
#
#     return