#!/usr/bin/env python
# coding=utf-8
"""
主题分析
"""

import re
from mzitu.runtimes.mzitu_suite import proxy_request


def get_max_page_num_of_theme(theme_url):
    html = proxy_request(theme_url)
    pattern = re.compile(r'<a class=(.+?)</span>(\d+)<span')
    page_num = pattern.findall(html)
    if not page_num:
        return 1
    else:
        max_page_num = page_num[-1][-1]
        return int(max_page_num)


def get_suite_urls_to_redis(theme_url):
    suite_url_list = []
    page_num = get_max_page_num_of_theme(theme_url)
    for i in range(1, page_num + 1):
        page_url = theme_url + 'page/{}/'.format(i)
        html = proxy_request(page_url)
        pattern = re.compile(r'<li(.+?) href=\"(.+?)\" target=')
        tmp_list = pattern.findall(html)
        suite_url_list += [x[1] for x in tmp_list]

    return suite_url_list
