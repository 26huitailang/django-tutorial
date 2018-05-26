import requests
import re
import time
import os
import random
import json
import threading
import glob

from mzitu.constants import (
    PROXY_SOURCE_URL,
    USER_AGENT_LIST,
    IMAGE_FOLDER,
)
from mzitu.runtimes.proxy_ip import GetProxyIp
from mzitu.runtimes.redis import RedisQueue
from mzitu.models import DownloadedSuit


mzitu_image_queue = RedisQueue('mzitu_image')
mzitu_url_queue = RedisQueue('mzitu_url')
MAX_DOWNLOAD_WORKER = 10


def get_max_page_num(html):
    pattern = re.compile(r'<span>(\d+)</span>')
    page_num = pattern.findall(html)
    print(page_num)
    return int(page_num[-1])


def header(referer):
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(USER_AGENT_LIST),
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers


def get_proxy_url(ip, port):
    proxy_url = "http://{}:{}".format(ip, port)
    return proxy_url


def proxy_request(url):
    flag = True
    page = None
    get_proxy_ip = GetProxyIp(PROXY_SOURCE_URL, random.choice(USER_AGENT_LIST))

    while flag:
        ip, port = get_proxy_ip.get_random_ip()
        try:
            time.sleep(0.5)
            proxy_url = get_proxy_url(ip, port)
            proxies = {"https": proxy_url}
            # proxies = {"http": proxy_url, "https": proxy_url}
            response = requests.get(url, proxies=proxies)
        except requests.exceptions.ProxyError as e:
            print(e)
            get_proxy_ip.mark_invalid_proxy_ip(ip, port)
        else:
            flag = False
            page = response.content.decode('utf-8')
            response.connection.close()

    return page


def get_image_urls(suit_url):
    suit_info = DownloadedSuit.objects.filter(url=suit_url).first()

    re_download = False
    if suit_info:
        print("该套牌已在DB中，确认是否存在，确认套图是否完整...")
        file_name = suit_info.name
        max_page_num = suit_info.max_page
        suit_folder = os.path.join(IMAGE_FOLDER, file_name)
        item_list = glob.glob('{}/*.jpg'.format(suit_folder))
        if len(item_list) >= max_page_num:
            print("已完整下载，跳过")
            return False
        else:
            print("该套图不完整，重新下载")
            re_download = True

    page = proxy_request(suit_url)

    max_page_num = get_max_page_num(page)
    title = re.search(r'class=\"main-title\">(.+?)</', page)
    title = title.group(1).strip()
    title = re.sub(r'[/\\:*?"<>|]', '-', title)  # windows 非法文件夹名字符
    print(title)

    folder = IMAGE_FOLDER
    folder = os.path.join(folder, title)

    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)

    # 保存下载内容到sqlite
    if re_download is False:
        suit_info = DownloadedSuit(
            name=title,
            url=suit_url,
            max_page=max_page_num,
        )
        suit_info.save()

    threads = []
    for i in range(1, max_page_num + 1):
        thread = threading.Thread(target=get_one_pic_url, args=(folder, i, suit_url,))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
    return


def get_one_pic_url(folder, i, suit_url):
    """分析一个图片的url，并放入redis队列"""
    filename = os.path.join(folder, "{:0>2d}.jpg".format(i))

    # urllib.request.urlretrieve(img_url, filename, check_rate)
    if os.path.isfile(filename):
        print("已存在：{}".format(filename))
        return

    time.sleep(0.5)
    url = suit_url + '/{}'.format(i)
    page = proxy_request(url)

    img_url = re.search(r'class=\"main-image(.+?)src=\"(.+?)\"', page)
    img_url = img_url.groups()[1]
    print(img_url)

    mzitu_image_queue.put(json.dumps({'filename': filename, 'url': img_url, 'header_url': url}))

    return


def requests_get(url, headers=None):
    get_proxy_ip = GetProxyIp(PROXY_SOURCE_URL, random.choice(USER_AGENT_LIST))

    ip, port = get_proxy_ip.get_random_ip()
    proxy_url = get_proxy_url(ip, port)
    proxies = {"https": proxy_url}

    return requests.get(url, headers=headers, proxies=proxies)


def download_images_to_local():

    while not mzitu_image_queue.empty():
        item = mzitu_image_queue.get()
        item = json.loads(item)

        if os.path.isfile(item['filename']):
            print("已存在：{}".format(item['filename']))
            continue

        img_bytes = requests_get(item['url'], headers=header(item['header_url']))
        with open(item['filename'], 'wb') as f:
            f.write(img_bytes.content)
        print("Downloaded {}".format(item['url']))
        time.sleep(1)

    return


def download_one_suit(suit_url):
    resp = get_image_urls(suit_url)
    if resp is False:
        return

    time.sleep(3)
    threads = []
    for i in range(MAX_DOWNLOAD_WORKER):
        thread = threading.Thread(target=download_images_to_local)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
