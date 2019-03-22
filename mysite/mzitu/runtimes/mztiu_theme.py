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
    assert check_theme_url(theme_url)
    suite_url_list = []
    page_num = get_max_page_num_of_theme(theme_url)
    for i in range(1, page_num + 1):
        page_url = theme_url + 'page/{}/'.format(i)
        html = proxy_request(page_url)
        pattern = re.compile(r'<li(.+?) href=\"(.+?)\" target=')
        tmp_list = pattern.findall(html)
        suite_url_list += [x[1] for x in tmp_list]

    return suite_url_list


def check_theme_url(url) -> bool:
    """检查是否是theme_url，是否是meituri url

    https://www.mzitu.com/tag/xiuren/
    https://www.mzitu.com/161751
    """
    pattern = r'https://www\.(.+?).com/(.+?)$'
    result = re.search(pattern, url)
    result_groups = result.groups()
    try:
        assert result_groups[0] == 'mzitu'
        assert 'tag' in result_groups[1]
    except AssertionError:
        return False
    return True
