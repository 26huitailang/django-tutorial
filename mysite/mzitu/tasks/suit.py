#!/usr/bin/env python
# coding=utf-8

import os
import re
import time
import json
import glob
import random
import requests
import threading
from bs4 import BeautifulSoup
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from mzitu.models.proxy_ip import ProxyIp
from mzitu.models.downloaded_suit import DownloadedSuit
from mzitu.constants import USER_AGENT_LIST
from mzitu.runtimes.redis import mzitu_image_queue
from mzitu.runtimes.proxy_ip import get_random_ip


logger = get_task_logger(__name__)

MAX_DOWNLOAD_WORKER = 10


# todo: refactor this page functions


def get_header(referer):
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
    """请求链接，返回页面html内容"""
    flag = True
    page = None

    while flag:
        ip, port = get_random_ip()
        try:
            time.sleep(0.5)
            proxy_url = get_proxy_url(ip, port)
            proxies = {"https": proxy_url}
            # proxies = {"http": proxy_url, "https": proxy_url}
            response = requests.get(url, proxies=proxies)
        except requests.exceptions.ProxyError as e:
            logger.error(e)
            ProxyIp.mark_proxy_ip_not_valid(ip, port)
        else:
            flag = False
            page = response.content.decode('utf-8')
            response.connection.close()

    return page


def get_max_page_num(html):
    """获取最大页码"""
    pattern = re.compile(r'<span>(\d+)</span>')
    page_num = pattern.findall(html)
    return int(page_num[-1])


def get_one_pic_url(suite_url, folder, i):
    """分析一个图片的url，并放入redis队列"""
    filename = os.path.join(folder, "{:0>2d}.jpg".format(i))

    # urllib.request.urlretrieve(img_url, filename, check_rate)
    if os.path.isfile(filename):
        print("已存在：{}".format(filename))
        return

    time.sleep(0.5)
    url = suite_url + '/{}'.format(i)
    page = proxy_request(url)

    img_url = re.search(r'class=\"main-image(.+?)src=\"(.+?)\"', page)
    img_url = img_url.groups()[1]
    print(img_url)

    mzitu_image_queue.put(json.dumps({'filename': filename, 'url': img_url, 'header_url': url}))

    return
def get_image_urls(suite_url):
    """获得图片的url"""
    suit_info = DownloadedSuit.objects.filter(url=suite_url).first()

    re_download = False
    if suit_info:
        print("该套牌已在DB中，确认是否存在，确认套图是否完整...")
        file_name = suit_info.name
        max_page_num = suit_info.max_page
        suit_folder = os.path.join(settings.IMAGE_FOLDER, file_name)
        item_list = glob.glob('{}/*.jpg'.format(suit_folder))
        if len(item_list) >= max_page_num:
            print("已完整下载，跳过")
            return False
        else:
            print("该套图不完整，重新下载")
            re_download = True

    page = proxy_request(suite_url)

    max_page_num = get_max_page_num(page)
    title = re.search(r'class=\"main-title\">(.+?)</', page)
    title = title.group(1).strip()
    title = re.sub(r'[/\\:*?"<>|]', '-', title)  # windows 非法文件夹名字符
    print(title)

    folder = settings.IMAGE_FOLDER
    folder = os.path.join(folder, title)

    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)

    # 保存下载内容到sqlite
    if re_download is False:
        suit_info = DownloadedSuit(
            name=title,
            url=suite_url,
            max_page=max_page_num,
        )
        suit_info.save()

    threads = []
    for i in range(1, max_page_num + 1):
        thread = threading.Thread(target=get_one_pic_url, args=(suite_url, folder, i,))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
    return


def requests_get(url, headers=None):
    """一个get请求"""
    ip, port = get_random_ip()
    proxy_url = get_proxy_url(ip, port)
    proxies = {"https": proxy_url}
    try:
        result = requests.get(url, headers=headers, proxies=proxies, timeout=5)
    except TimeoutError:
        print("Timeout: {}".format(url))
        result = None

    return result


def download_images_to_local():
    """下载到磁盘"""
    while not mzitu_image_queue.empty():
        item = mzitu_image_queue.get()
        item = json.loads(item)

        if os.path.isfile(item['filename']):
            print("已存在：{}".format(item['filename']))
            continue

        img_bytes = requests_get(item['url'], headers=get_header(item['header_url']))
        if img_bytes is None:
            continue

        with open(item['filename'], 'wb') as f:
            f.write(img_bytes.content)
        print("Downloaded {}".format(item['url']))
        time.sleep(1)

    return


@shared_task
def download_one_suit(suite_url):
    resp = get_image_urls(suite_url)
    if resp is False:
        return

    time.sleep(3)

    # 打开对应的文件夹
    os.system("start explorer {}".format(settings.IMAGE_FOLDER.replace('/', '\\')))

    threads = []
    for i in range(MAX_DOWNLOAD_WORKER):
        thread = threading.Thread(target=download_images_to_local)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
