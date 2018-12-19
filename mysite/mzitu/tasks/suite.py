#!/usr/bin/env python
# coding=utf-8

import os
import re
import time
import json
import glob
import threading
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from django_vises.runtimes.instance_serializer import serialize_instance, unserialize_object

from mzitu.models.downloaded_suit import DownloadedSuit
from mzitu.runtimes.redis import mzitu_image_queue
from mzitu.runtimes.suite import requests_get, proxy_request, generate_headers, PicJsonRedis

logger = get_task_logger(__name__)

MAX_DOWNLOAD_WORKER = 6


# todo: refactor this page functions


def get_max_page_num_of_suite(html):
    """获取suite下image最大页码"""
    pattern = re.compile(r'<span>(\d+)</span>')
    page_num = pattern.findall(html)
    return int(page_num[-1])


def get_one_pic_url(suite_url, suite_folder, nth_pic):
    """分析一个图片的url，并放入redis队列"""
    pic_full_path = os.path.join(suite_folder, "{:0>2d}.jpg".format(nth_pic))

    if os.path.isfile(pic_full_path):
        # image已经存在
        print("已存在：{}".format(pic_full_path))
        return

    time.sleep(0.5)
    page_url = suite_url + '/{}'.format(nth_pic)
    page = proxy_request(page_url)

    img_url = re.search(r'class=\"main-image(.+?)src=\"(.+?)\"', page)
    img_url = img_url.groups()[1]
    print(img_url)

    pic_instance = PicJsonRedis(pic_full_path, img_url, page_url)
    mzitu_image_queue.put(json.dumps(pic_instance, default=serialize_instance))

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

    max_page_num = get_max_page_num_of_suite(page)
    title = re.search(r'class=\"main-title\">(.+?)</', page)
    title = title.group(1).strip()
    title = re.sub(r'[/\\:*?"<>|]', '-', title)  # windows 非法文件夹名字符
    print(title)

    suite_folder = settings.IMAGE_FOLDER
    suite_folder = os.path.join(suite_folder, title)

    if not os.path.isdir(suite_folder):
        os.makedirs(suite_folder, exist_ok=True)

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
        thread = threading.Thread(target=get_one_pic_url, args=(suite_url, suite_folder, i,))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
    return


def download_images_to_local():
    """下载到磁盘"""
    while not mzitu_image_queue.empty():
        item = mzitu_image_queue.get()
        pic_instance = json.loads(item, object_hook=unserialize_object)

        if os.path.isfile(pic_instance.full_path):
            logger.info("已存在：{}".format(pic_instance.full_path))
            continue

        img_bytes = None
        while not img_bytes:
            img_bytes = requests_get(pic_instance.url, headers=generate_headers(pic_instance.header_referer))

        with open(pic_instance.full_path, 'wb') as f:
            f.write(img_bytes.content)
        logger.info("Downloaded {}".format(pic_instance.url))
        time.sleep(1)

    return


@shared_task
def download_one_suite(suite_url):
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
