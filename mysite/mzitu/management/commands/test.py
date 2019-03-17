# coding: utf-8

from django.core.management.base import BaseCommand
from mzitu.models.downloaded_suite import DownloadedSuite
from django.conf import settings
import shutil
import os
import time
from mzitu.runtimes.meituri_suite import MeituriSuite
import requests
from lxml import etree
from queue import Queue

q = Queue()

class Command(BaseCommand):
    help = '将测试websocket用的图置为初始状态，未完成并删除本地文件'
    def handle(self, *args, **options):
        suite_url = 'https://www.meituri.com/a/25133/'
        other_page_url_template = suite_url + '{}.html'

        meituri_suite = MeituriSuite(suite_url)
        a = requests.get(meituri_suite.suite_url)
        html_etree = etree.HTML(a.content.decode('utf-8'))
        # max page
        page_tags = html_etree.xpath('//div[@id="pages"]/a[last()-1]')
        max_page = int(page_tags[0].text.strip())

        # first page
        self.get_img_url(html_etree)
        # second to last
        for i in range(2, max_page + 1):
            # 获取img_url, name
            response = requests.get(other_page_url_template.format(i))
            _html_etree = etree.HTML(response.content.decode('utf-8'))
            self.get_img_url(_html_etree)
        self.download_imgs_in_queue()

        return

    def get_img_url(self, html_etree):
        img_tags = html_etree.xpath('//div[@class="content"]/img')
        for i in img_tags:
            url = i.attrib["src"]
            img_name = i.attrib["alt"]
            path = os.path.join(settings.IMAGE_FOLDER_MEITURI, img_name)
            print(f'{url} {img_name}')
            self.put_img_url_path_to_queue(url, path)

    def put_img_url_path_to_queue(self, url, path):
        q.put((url, path))
        return

    def download_one_img_to_local(self, url, path):
        img_bytes = requests.get(url, timeout=(5, 30))

        with open(path, 'wb') as f:
            f.write(img_bytes.content)
        return

    def download_imgs_in_queue(self):
        self.mkdir_if_folder_not_exist(settings.IMAGE_FOLDER_MEITURI)
        while not q.empty():
            item = q.get()
            url = item[0]
            path = item[1]
            if not os.path.isfile(path):
                self.download_one_img_to_local(url, path)
            time.sleep(2)

    def mkdir_if_folder_not_exist(self, path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

#todo: 标题/tags/持久化等