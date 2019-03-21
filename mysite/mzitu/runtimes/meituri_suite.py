# coding: utf-8

import os
import time
import requests
from queue import Queue
from pprint import pprint
from requests_html import HTMLSession, HTMLResponse
from django.conf import settings
from django.db import IntegrityError
from mzitu.models.downloaded_suite import DownloadedSuite, SuiteImageMap
from mzitu.models.tag import Tag
# todo: 持久化等, 继承代理请求，不然并发会有影响
import logging

logger = logging.getLogger(__name__)


def _check_init(f):
    """装饰器，看MeituriSuite是否有初始化"""
    def wrapper(self, *args, **kwargs):
        if self.response is None:
            raise ValueError('self.response is None, u should first init')
        assert isinstance(self.response, HTMLResponse)
        return f(self, *args, **kwargs)

    return wrapper


class MeituriBase(object):

    def __init__(self):
        self.response = None

    def get_response_with_url(self, url) -> HTMLResponse:
        """根据url返回response obj"""
        session = HTMLSession()
        response = session.get(url)
        assert isinstance(response, HTMLResponse)
        return response

    @_check_init
    def get_max_page(self) -> int:
        """获得suite最大页码"""
        max_page_str = self.response.html.find('#pages a')[-2].text
        max_page = int(max_page_str)
        return max_page


class MeituriSuite(MeituriBase):
    """一个suite"""

    def __init__(self, first_suite_url):
        super(MeituriSuite).__init__()
        self.prefix = 'meituri_'
        # self.response = None
        self.first_suite_url = first_suite_url
        self.other_page_url_template = self.first_suite_url + '{}.html'
        self.max_page = None
        self.title = None
        self.organization = None
        self.img_queue = Queue()
        self.suite_obj = None

    def init(self):
        """调用这个通过首页初始化一些必要的参数

        手动调用，避免实例话的时候就产生request
        """
        self.response = self.get_response_with_url(self.first_suite_url)
        self.max_page = self.get_max_page()
        self.title = self.get_title()
        self.tags = self.get_tags()
        self.organization = self.get_organization()
        # 如果没有创建
        is_exist, suite_obj = DownloadedSuite.is_url_exist(self.first_suite_url)
        if not is_exist:
            suite_obj = DownloadedSuite.objects.create(
                name=self.title,
                url=self.first_suite_url,
                max_page=self.max_page,
            )
            tag_instances = []
            for tag_name, href in self.tags:
                tag_instance, _ = Tag.objects.update_or_create(name=tag_name, defaults={'url': href})
                tag_instances.append(tag_instance)
            suite_obj.tags.set(tag_instances)
        self.suite_obj = suite_obj
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

    def get_img_url(self, response: HTMLResponse):
        """获取一页中的img url，并放入queue"""
        div_content = response.html.find('.content', first=True)
        img_elements = div_content.find('img')
        for i in img_elements:
            url = i.attrs["src"]
            img_name = i.attrs["alt"] + '.' + url.split('.')[-1]
            path = os.path.join(settings.IMAGE_FOLDER_MEITURI, self.organization, self.title, img_name)
            # 存入db
            try:
                SuiteImageMap.objects.create(
                    suite=self.suite_obj,
                    url=url,
                    image=SuiteImageMap.get_image_path('meituri',
                                                       self.suite_obj.name,
                                                       path.split('/')[-1],
                                                       org=self.organization)
                )
                logger.info('{} {}'.format(url, path))
            except IntegrityError as e:
                logger.warning(e)
            self.put_img_url_path_to_queue(url, path)

    def put_img_url_path_to_queue(self, url, path):
        self.img_queue.put((url, path))
        return

    @_check_init
    def get_imgs_and_download(self, do_download: bool = True, time_gap=5):
        # first page
        self.get_img_url(self.response)
        # second to last
        for i in range(2, self.max_page + 1):
            time.sleep(time_gap)
            # 获取img_url, name
            response = self.get_response_with_url(self.other_page_url_template.format(i))
            self.get_img_url(response)
        if do_download:
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
        # meituri folder check
        self.mkdir_if_folder_not_exist(settings.IMAGE_FOLDER_MEITURI)
        while not self.img_queue.empty():
            item = self.img_queue.get()
            url = item[0]
            path = item[1]
            suite_folder = '/'.join(path.split('/')[:-1])
            # 当前suite folder check
            self.mkdir_if_folder_not_exist(suite_folder)
            # 没有才下载
            if not os.path.isfile(path):
                logger.info('path ownloading: %s', path)
                self._download_one_img_to_local(url, path)
            else:
                logger.info('path exist: %s', path)

    def mkdir_if_folder_not_exist(self, path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)


class MeituriTheme(MeituriBase):
    """多页多个suite"""

    def __init__(self, first_theme_url):
        super(MeituriTheme).__init__()
        self.first_theme_url = first_theme_url
        # self.other_page_url_template = self.first_theme_url + 'index_{}.html'
        self.next_page_theme_url = None
        # 拿不到max_page，改用下一页的连接
        self.suite_queue = Queue()
        # self.response = None
        pass

    def init(self):
        """请求theme_url初始化一些内容"""
        self.response = self.get_response_with_url(self.first_theme_url)
        return

    def get_next_page_url(self, response: HTMLResponse):
        next_url_element = response.html.find('#pages .next')[0]
        if next_url_element.text == '上一页':
            self.next_page_theme_url = None
        elif next_url_element.text == '下一页':
            next_url = next_url_element.absolute_links.pop()
            self.next_page_theme_url = next_url
        else:
            raise ValueError(next_url_element.text)

    def get_one_page_suite_url_to_queue(self, response: HTMLResponse) -> list:
        a_elements = response.html.find('.biaoti a')
        suite_urls = [x.attrs['href'] for x in a_elements]
        self.put_suite_urls_to_queue(suite_urls)
        pprint(suite_urls)
        return suite_urls

    def should_put_url_to_queue(self, url) -> bool:
        """url是否推到队列中

        :return:
            `False` 已完成
            `True` 其他情况
        """
        is_complete = DownloadedSuite.is_url_completed(url)
        if is_complete:
            return False
        return True

    def put_suite_urls_to_queue(self, urls):
        for url in urls:
            if self.should_put_url_to_queue(url):
                self.suite_queue.put(url)
                logger.debug('put url to queue: %s', url)
        return

    def get_all_suite_urls_to_queue(self, time_gap=5):
        # 获取page，index_1.html为第二页
        page = 1
        while True:
            logger.info('page: %s', page)
            if page == 1:
                html_response = self.response
            else:
                html_response = self.get_response_with_url(self.next_page_theme_url)
            self.get_one_page_suite_url_to_queue(html_response)

            # 判断break，放后面，放前面会导致一页的内容提前结束
            self.get_next_page_url(html_response)
            if self.next_page_theme_url is None:
                break
            time.sleep(time_gap)
            page += 1
        return
