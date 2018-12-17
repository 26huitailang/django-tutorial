import requests
import re
import time
import os
import random
import json
import threading
import glob

from mzitu.constants import USER_AGENT_LIST
from mzitu.runtimes.redis import mzitu_image_queue
from mzitu.models.downloaded_suit import DownloadedSuit


class MzituBase:

    def get_proxy_url(self, ip, port):
        proxy_url = "http://{}:{}".format(ip, port)
        return proxy_url

    def proxy_request(self, url):
        flag = True
        page = None

        while flag:
            ip, port = self.get_proxy_ip.get_random_ip()
            try:
                time.sleep(0.5)
                proxy_url = self.get_proxy_url(ip, port)
                proxies = {"https": proxy_url}
                # proxies = {"http": proxy_url, "https": proxy_url}
                response = requests.get(url, proxies=proxies)
            except requests.exceptions.ProxyError as e:
                print(e)
                self.get_proxy_ip.mark_invalid_proxy_ip(ip, port)
            else:
                flag = False
                page = response.content.decode('utf-8')
                response.connection.close()

        return page


class MzituOneSuite(MzituBase):

    MAX_DOWNLOAD_WORKER = 10

    def __init__(self, suite_url):
        self.suite_url = suite_url

    def get_max_page_num(self, html):
        pattern = re.compile(r'<span>(\d+)</span>')
        page_num = pattern.findall(html)
        return int(page_num[-1])

    def proxy_request(self, url):
        """请求链接，返回页面html内容"""
        flag = True
        page = None

        while flag:
            ip, port = self.get_proxy_ip.get_random_ip()
            try:
                time.sleep(0.5)
                proxy_url = self.get_proxy_url(ip, port)
                proxies = {"https": proxy_url}
                # proxies = {"http": proxy_url, "https": proxy_url}
                response = requests.get(url, proxies=proxies)
            except requests.exceptions.ProxyError as e:
                print(e)
                self.get_proxy_ip.mark_invalid_proxy_ip(ip, port)
            else:
                flag = False
                page = response.content.decode('utf-8')
                response.connection.close()

        return page

    def header(self, referer):
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

    def get_image_urls(self):
        suit_info = DownloadedSuit.objects.filter(url=self.suite_url).first()

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

        page = self.proxy_request(self.suite_url)

        max_page_num = self.get_max_page_num(page)
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
                url=self.suite_url,
                max_page=max_page_num,
            )
            suit_info.save()

        threads = []
        for i in range(1, max_page_num + 1):
            thread = threading.Thread(target=self.get_one_pic_url, args=(folder, i,))
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()
        return

    def get_one_pic_url(self, folder, i):
        """分析一个图片的url，并放入redis队列"""
        filename = os.path.join(folder, "{:0>2d}.jpg".format(i))

        # urllib.request.urlretrieve(img_url, filename, check_rate)
        if os.path.isfile(filename):
            print("已存在：{}".format(filename))
            return

        time.sleep(0.5)
        url = self.suite_url + '/{}'.format(i)
        page = self.proxy_request(url)

        img_url = re.search(r'class=\"main-image(.+?)src=\"(.+?)\"', page)
        img_url = img_url.groups()[1]
        print(img_url)

        mzitu_image_queue.put(json.dumps({'filename': filename, 'url': img_url, 'header_url': url}))

        return

    def requests_get(self, url, headers=None):
        get_proxy_ip = GetProxyIp(PROXY_SOURCE_URL, random.choice(USER_AGENT_LIST))

        ip, port = get_proxy_ip.get_random_ip()
        proxy_url = self.get_proxy_url(ip, port)
        proxies = {"https": proxy_url}
        try:
            result = requests.get(url, headers=headers, proxies=proxies, timeout=5)
        except TimeoutError:
            print("Timeout: {}".format(url))
            result = None

        return result

    def download_images_to_local(self):

        while not mzitu_image_queue.empty():
            item = mzitu_image_queue.get()
            item = json.loads(item)

            if os.path.isfile(item['filename']):
                print("已存在：{}".format(item['filename']))
                continue

            img_bytes = self.requests_get(item['url'], headers=self.header(item['header_url']))
            if img_bytes is None:
                continue

            with open(item['filename'], 'wb') as f:
                f.write(img_bytes.content)
            print("Downloaded {}".format(item['url']))
            time.sleep(1)

        return

    def download_one_suit(self):
        resp = self.get_image_urls()
        if resp is False:
            return

        time.sleep(3)

        # 打开对应的文件夹
        os.system("start explorer {}".format(IMAGE_FOLDER.replace('/', '\\')))

        threads = []
        for i in range(self.MAX_DOWNLOAD_WORKER):
            thread = threading.Thread(target=self.download_images_to_local)
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()


class MzituThemePage(MzituBase):

    def __init__(self, theme_url):
        self.theme_url = theme_url

    def get_max_page_num(self):
        html = self.proxy_request(self.theme_url)
        # print(html)
        pattern = re.compile(r'<a class=(.+?)</span>(\d+)<span')
        page_num = pattern.findall(html)
        # print(page_num)
        if not page_num:
            return 1
        else:
            max_page_num = page_num[-1][-1]
            return int(max_page_num)

    def get_suite_urls_to_redis(self):
        suite_url_list = []
        for i in range(1, self.get_max_page_num() + 1):
            page_url = self.theme_url + 'page/{}/'.format(i)
            html = self.proxy_request(page_url)
            pattern = re.compile(r'<li(.+?) href=\"(.+?)\" target=')
            tmp_list = pattern.findall(html)
            # print(tmp_list, len(tmp_list))
            suite_url_list += [x[1] for x in tmp_list]

        return suite_url_list
