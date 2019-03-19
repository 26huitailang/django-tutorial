# coding: utf-8

from mzitu.models.downloaded_suite import DownloadedSuite
from django.conf import settings
import shutil
import os
import time
import requests
from lxml import etree
from queue import Queue
from requests_html import HTMLSession


def _check_init(f):
    def wrapper(self, *args, **kwargs):
        if self.response is None:
            raise ValueError('self.response is None, u should first init_with_first_page')
        return f(self, *args, **kwargs)

    return wrapper


class MeituriSuite(object):

    def __init__(self, first_suite_url):
        self.prefix = 'meituri_'
        self.response = None
        self.first_suite_url = first_suite_url
        self.other_page_url_template = self.first_suite_url + '{}.html'
        self.max_page = None
        self.title = None
        self.organization = None
        self.queue = Queue()

    def init_with_first_page(self):
        """调用这个通过首页初始化一些必要的参数

        手动调用，避免实例话的时候就产生request
        """
        self.response = self.get_response_with_url(self.first_suite_url)
        self.max_page = self.get_max_page()
        self.title = self.get_title()
        self.tags = self.get_tags()
        self.organization = self.get_organization()
        return

    @_check_init
    def get_organization(self) -> str:
        """机构"""
        return self.response.html.find('p a', first=True).text

    @_check_init
    def get_tags(self) -> list:
        """获取标签，列表

        [(tag_name, tag_url), ...]
        """
        tags_elements = self.response.html.find('.fenxiang_l a')
        return [(self.prefix + x.text, x.attrs['href']) for x in tags_elements]

    @_check_init
    def get_title(self):
        """获取标题"""
        title = self.response.html.find('h1', first=True).text
        return title

    @_check_init
    def get_max_page(self) -> int:
        """获得suite最大页码"""
        max_page_str = self.response.html.find('#pages a')[-2].text
        max_page = int(max_page_str)
        return max_page

    def get_response_with_url(self, url):
        """根据url返回etree解析结果"""
        session = HTMLSession()
        response = session.get(url)
        return response

    def get_img_url(self, response):
        """获取一页中的img url，并放入queue"""
        div_content = response.html.find('.content', first=True)
        img_elements = div_content.find('img')
        for i in img_elements:
            url = i.attrs["src"]
            img_name = i.attrs["alt"] + '.' + url.split('.')[-1]
            path = os.path.join(settings.IMAGE_FOLDER_MEITURI, self.organization, self.title, img_name)
            print(f'{url} {img_name}')
            self.put_img_url_path_to_queue(url, path)

    def put_img_url_path_to_queue(self, url, path):
        self.queue.put((url, path))
        return

    @_check_init
    def get_imgs_and_download(self):
        # first page
        self.get_img_url(self.response)
        # second to last
        for i in range(2, self.max_page + 1):
            # 获取img_url, name
            response = self.get_response_with_url(self.other_page_url_template.format(i))
            self.get_img_url(response)
        self._download_imgs_in_queue()

    def _download_one_img_to_local(self, url, path, sleep_after=2):
        img_bytes = requests.get(url, timeout=(5, 30))

        with open(path, 'wb') as f:
            f.write(img_bytes.content)
        print(f'downloaded: {path}')
        time.sleep(sleep_after)
        return

    def _download_imgs_in_queue(self):
        """从queue获取要下载的img"""
        self.mkdir_if_folder_not_exist(settings.IMAGE_FOLDER_MEITURI)
        while not self.queue.empty():
            item = self.queue.get()
            url = item[0]
            path = item[1]
            suite_folder = '/'.join(path.split('/')[:-1])
            self.mkdir_if_folder_not_exist(suite_folder)
            if not os.path.isfile(path):
                self._download_one_img_to_local(url, path)

    def mkdir_if_folder_not_exist(self, path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

# todo: 持久化等
