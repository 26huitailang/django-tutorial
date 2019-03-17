#!/usr/bin/env python
# coding=utf-8

import os
import time
import glob
import random
import logging
import requests
import re
import json
import threading
from django.conf import settings
from django.db import IntegrityError

from django_vises.runtimes.instance_serializer import serialize_instance, unserialize_object
from mzitu.models.downloaded_suite import DownloadedSuite, SuiteImageMap
from mzitu.models.tag import Tag
from mzitu.models.proxy_ip import ProxyIp
from mzitu.runtimes.redis import mzitu_image_queue, PicJsonRedis
from mzitu.runtimes.proxy_ip import get_random_ip
from mzitu.constants import USER_AGENT_LIST

logger = logging.getLogger(__name__)


# def generate_proxies(ip, port) -> str:
#     """构建proxy_url"""
#     proxy_url = "http://{}:{}".format(ip, port)
#     return proxy_url


def generate_proxies(ip, port) -> dict:
    """构建proxies"""
    proxies = {
        'http': 'http://{}:{}'.format(ip, port),
        'https': 'https://{}:{}'.format(ip, port),
    }
    return proxies


def requests_get(url, headers=None):
    """利用代理ip构建的requests.get请求"""
    # todo: 重试机制
    ip, port = get_random_ip()
    proxies = generate_proxies(ip, port)
    try:
        result = requests.get(url, headers=headers, proxies=proxies, timeout=(5, 30))
    except Exception as e:  # todo: 更精准的捕获
        print("{} {}".format(url, e))
        result = None

    return result


def proxy_request(url):
    """请求链接，返回页面html内容"""
    flag = True
    page = None

    while flag:
        ip, port = get_random_ip()
        try:
            time.sleep(0.5)
            proxies = generate_proxies(ip, port)
            response = requests.get(url, proxies=proxies, timeout=(5, 30))
        except Exception as e:
            logger.error(e)
            ProxyIp.set_score_change(ip, port, -1)
        else:
            flag = False
            page = response.content.decode('utf-8')
            response.close()

    return page


def generate_headers(referer):
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


def get_local_suite_img_list(suite_name: str = None) -> list:
    """获取本地suite的图片列表"""
    if suite_name is None:
        return []
    suite_path = os.path.join(settings.IMAGE_FOLDER_MZITU, suite_name)
    img_file_list = glob.glob('{}/*.jpg'.format(suite_path))
    return img_file_list


def get_local_suite_count(suite_name: str = None) -> int:
    """本地suite图片数量"""
    return len(get_local_suite_img_list(suite_name))


class MeituriSuite:
    """对mzitu的suite相关操作的定义"""

    def __init__(self, suite_url, max_download_worker=5):
        self.suite_url = suite_url
        self.max_download_worker = max_download_worker

    def get_one_suite_and_download(self):
        resp = self.get_suite_pages_and_start_threads()
        # 如果重复的话resp是False，其他为None
        if resp is False:
            return

        time.sleep(3)

        # 打开对应的文件夹
        # os.system("start explorer {}".format(settings.IMAGE_FOLDER.replace('/', '\\')))

        # todo: 流程可以改为解析成每页后，就用gevent分发任务了，是否下载可以用一个bool控制，不用单独下载程序
        # todo: 现在暂时不用gevent，会造成栈溢出
        threads = []
        for i in range(self.max_download_worker):
            thread = threading.Thread(target=self.download_images_to_local)
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()

        # 下载完将suite 完整性置为True
        suite_obj = DownloadedSuite.objects.filter(url=self.suite_url, is_complete=False).first()
        if suite_obj is None:
            return

        if suite_obj.max_page == get_local_suite_count(suite_obj.name):
            suite_obj.is_complete = True
            suite_obj.save()
        return

    def get_suite_pages_and_start_threads(self):
        """判断suite是否完整，获得每页的url，启动threads分析每页"""
        page_content = proxy_request(self.suite_url)

        max_page_num = self.parse_max_page_num_of_suite(page_content)
        title = self.parse_suite_title(page_content)
        logger.debug(title)

        suite_folder = settings.IMAGE_FOLDER_MEITURI
        suite_folder = os.path.join(suite_folder, title)
        if not os.path.isdir(suite_folder):
            # folder 创建
            os.makedirs(suite_folder, exist_ok=True)

        suite_instance, is_created = DownloadedSuite.objects.get_or_create(
            name=title,
            defaults={'url': self.suite_url, 'max_page': max_page_num}
        )

        # 获取tags
        if not suite_instance.tags.all():
            tags_href_and_name = self.parse_tags_of_suite(page_content)
            tag_instances = []
            for href, name in tags_href_and_name:
                tag_instance, _ = Tag.objects.update_or_create(name=name, defaults={'url': href})
                tag_instances.append(tag_instance)
            suite_instance.tags.set(tag_instances)

        if is_created is False:
            # 如果数据库有记录，则看看本地文件是否完整
            print("该套牌已在DB中，确认是否存在，确认套图是否完整...")
            suite_name = suite_instance.name
            max_page_num = suite_instance.max_page
            img_local_file_count = get_local_suite_count(suite_name)
            img_obj_count = SuiteImageMap.objects.filter(suite__id=suite_instance.id).count()
            if img_local_file_count >= max_page_num and img_obj_count == suite_instance.max_page:
                # 本地文件数量匹配，img数据库完整
                print("已完整下载，跳过")
                return False
            else:
                print("该套图不完整，重新下载")

        # 分析每页
        # todo: 可以和download_one_suite的threads部分合并为一个threads启动器
        threads = []
        for i in range(1, max_page_num + 1):
            thread = threading.Thread(target=self.get_one_pic_url, args=(suite_folder, i,))
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()
        return

    def get_one_pic_url(self, suite_folder, nth_pic):
        """分析一个图片的url，并放入redis队列"""
        pic_full_path = os.path.join(suite_folder, "{:0>2d}.jpg".format(nth_pic))

        # if os.path.isfile(pic_full_path):
        #     image已经存在
        #     print("已存在：{}".format(pic_full_path))
        #     return

        time.sleep(0.5)
        page_url = self.suite_url + '/{}'.format(nth_pic)
        page_content = proxy_request(page_url)
        img_url = self.parse_img_url(page_content)
        print(img_url)

        # suite_url 用于后面标示map的外键
        pic_instance = PicJsonRedis(pic_full_path, img_url, page_url, self.suite_url)
        mzitu_image_queue.put(json.dumps(pic_instance, default=serialize_instance))

        return

    @staticmethod
    def parse_max_page_num_of_suite(html):
        """获取suite下image最大页码"""
        pattern = re.compile(r'<span>(\d+)</span>')
        page_num = pattern.findall(html)
        return int(page_num[-1])

    @staticmethod
    def parse_tags_of_suite(page_content):
        """获取套图的tags和tag href"""
        tags_pattern = r'class=\"main-tags(.+?)</span>(.+?)</div>'
        tags_result = re.search(tags_pattern, page_content)
        tags_html_text = tags_result.groups()[1]
        a_pattern = r'href=\"(.+?)\"(.+?)>(.+?)</a>'
        a_result = re.findall(a_pattern, tags_html_text)
        href_and_name = [(x[0], x[2]) for x in a_result]

        return href_and_name

    @staticmethod
    def parse_img_url(page_content):
        """解析图片url"""
        img_url = re.search(r'class=\"main-image(.+?)src=\"(.+?)\"', page_content)
        img_url = img_url.groups()[1]
        return img_url

    @staticmethod
    def parse_suite_title(page_content):
        """解析suite的title"""
        title = re.search(r'class=\"main-title\">(.+?)</', page_content)
        title = title.group(1).strip()
        title = re.sub(r'[/\\:*?"<>|]', '-', title)  # windows 非法文件夹名字符
        return title

    @staticmethod
    def download_images_to_local():
        """下载到磁盘"""
        while not mzitu_image_queue.empty():
            item = mzitu_image_queue.get()
            pic_instance = json.loads(item, object_hook=unserialize_object)

            suite_obj = DownloadedSuite.objects.filter(url=pic_instance.suite_url).first()
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

            if os.path.isfile(pic_instance.full_path):
                logger.info("已存在：{}".format(pic_instance.full_path))
                continue

            img_bytes = None
            while not img_bytes:
                img_bytes = requests_get(pic_instance.url, headers=generate_headers(pic_instance.header_referer))

            with open(pic_instance.full_path, 'wb') as f:
                f.write(img_bytes.content)

            logger.info("Downloaded {}".format(pic_instance.url))
            time.sleep(0.5)

        return
