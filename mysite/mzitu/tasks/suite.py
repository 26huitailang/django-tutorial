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
from django.db import IntegrityError

from django_vises.runtimes.instance_serializer import serialize_instance, unserialize_object

from mzitu.models.downloaded_suite import DownloadedSuite, SuiteImageMap
from mzitu.models.tag import Tag
from mzitu.runtimes.redis import mzitu_image_queue
from mzitu.runtimes.suite import requests_get, proxy_request, generate_headers, PicJsonRedis

logger = get_task_logger(__name__)

MAX_DOWNLOAD_WORKER = 5


# todo: refactor this page functions


def parse_max_page_num_of_suite(html):
    """获取suite下image最大页码"""
    pattern = re.compile(r'<span>(\d+)</span>')
    page_num = pattern.findall(html)
    return int(page_num[-1])


def parse_tags_of_suite(page_content):
    """获取套图的tags和tag href"""
    tags_pattern = r'class=\"main-tags(.+?)</span>(.+?)</div>'
    tags_result = re.search(tags_pattern, page_content)
    tags_html_text = tags_result.groups()[1]
    a_pattern = r'href=\"(.+?)\"(.+?)>(.+?)</a>'
    a_result = re.findall(a_pattern, tags_html_text)
    href_and_name = [(x[0], x[2]) for x in a_result]

    return href_and_name


def parse_img_url(page_content):
    """解析图片url"""
    img_url = re.search(r'class=\"main-image(.+?)src=\"(.+?)\"', page_content)
    img_url = img_url.groups()[1]
    return img_url


def parse_suite_title(page_content):
    """解析suite的title"""
    title = re.search(r'class=\"main-title\">(.+?)</', page_content)
    title = title.group(1).strip()
    title = re.sub(r'[/\\:*?"<>|]', '-', title)  # windows 非法文件夹名字符
    return title


def get_one_pic_url(suite_url, suite_folder, nth_pic):
    """分析一个图片的url，并放入redis队列"""
    pic_full_path = os.path.join(suite_folder, "{:0>2d}.jpg".format(nth_pic))

    if os.path.isfile(pic_full_path):
        # image已经存在
        print("已存在：{}".format(pic_full_path))
        return

    time.sleep(0.5)
    page_url = suite_url + '/{}'.format(nth_pic)
    page_content = proxy_request(page_url)
    img_url = parse_img_url(page_content)
    print(img_url)

    # suite_url 用于后面标示map的外键
    pic_instance = PicJsonRedis(pic_full_path, img_url, page_url, suite_url)
    mzitu_image_queue.put(json.dumps(pic_instance, default=serialize_instance))

    return


def get_suite_pages_and_start_threads(suite_url):
    """判断suite是否完整，获得每页的url，启动threads分析每页"""
    page_content = proxy_request(suite_url)

    max_page_num = parse_max_page_num_of_suite(page_content)
    title = parse_suite_title(page_content)
    logger.debug(title)

    suite_folder = settings.IMAGE_FOLDER
    suite_folder = os.path.join(suite_folder, title)
    if not os.path.isdir(suite_folder):
        # folder 创建
        os.makedirs(suite_folder, exist_ok=True)

    suite_instance, is_created = DownloadedSuite.objects.get_or_create(
        name=title,
        defaults={'url': suite_url, 'max_page': max_page_num}
    )

    # 获取tags
    if not suite_instance.tags.all():
        tags_href_and_name = parse_tags_of_suite(page_content)
        tag_instances = []
        for href, name in tags_href_and_name:
            tag_instance, _ = Tag.objects.update_or_create(name=name, defaults={'url': href})
            tag_instances.append(tag_instance)
        suite_instance.tags.set(tag_instances)

    if is_created is False:
        # 如果数据库有记录，则看看本地文件是否完整
        print("该套牌已在DB中，确认是否存在，确认套图是否完整...")
        file_name = suite_instance.name
        max_page_num = suite_instance.max_page
        suit_folder = os.path.join(settings.IMAGE_FOLDER, file_name)
        item_list = glob.glob('{}/*.jpg'.format(suit_folder))
        if len(item_list) >= max_page_num:
            # 文件数量匹配
            print("已完整下载，跳过")
            return False
        else:
            print("该套图不完整，重新下载")

    # 分析每页
    # todo: 可以和download_one_suite的threads部分合并为一个threads启动器
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

        suite_obj = DownloadedSuite.objects.get(url=pic_instance.suite_url)
        suite_image_map = SuiteImageMap(
            suite=suite_obj,
            url=pic_instance.url,
            image=SuiteImageMap.get_image_path(
                suite_obj.name,
                pic_instance.full_path.split('/')[-1],  # filename
            )
        )
        try:
            suite_image_map.save()
        except IntegrityError as e:
            logger.warning(e)
        logger.info("Downloaded {}".format(pic_instance.url))
        time.sleep(0.5)

    return


@shared_task
def download_one_suite(suite_url):
    resp = get_suite_pages_and_start_threads(suite_url)
    # 如果重复的话resp是False，其他为None
    if resp is False:
        return

    time.sleep(3)

    # 打开对应的文件夹
    # os.system("start explorer {}".format(settings.IMAGE_FOLDER.replace('/', '\\')))

    threads = []
    for i in range(MAX_DOWNLOAD_WORKER):
        thread = threading.Thread(target=download_images_to_local)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
