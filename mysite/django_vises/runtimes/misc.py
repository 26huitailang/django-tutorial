#!/usr/bin/env python
# coding=utf-8

# import glob
import os
import operator
from django.utils.six import text_type

# copy from rest_framework
# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'


def get_request_client_ip_address(request):
    """获取 request 请求来源 ip address, 支持 nginx 使用 X-Real-IP/X-FORWARDED-FOR 传递来源 ip 地址
    """
    ip = request.META.get('X-Real-IP') or request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, text_type):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


def get_authorization_token_from_header(request):
    """
    Return request's 'Authorization:' token

    """
    keyword = 'Token'
    auth = get_authorization_header(request).split()

    if not auth or auth[0].lower() != keyword.lower().encode():
        return None

    # if len(auth) == 1:
    #     msg = _('Invalid token header. No credentials provided.')
    #     raise exceptions.AuthenticationFailed(msg)
    # elif len(auth) > 2:
    #     msg = _('Invalid token header. Token string should not contain spaces.')
    #     raise exceptions.AuthenticationFailed(msg)
    #
    # try:
    #     token = auth[1].decode()
    # except UnicodeError:
    #     msg = _('Invalid token header. Token string should not contain invalid characters.')
    #     raise exceptions.AuthenticationFailed(msg)
    if len(auth) != 2:
        return None

    try:
        token = auth[1].decode()
    except UnicodeError:
        return None

    return token


def str_to_boolean(text):
    """将字符转为布尔值，if条件可以扩展"""
    if text.lower() in ['false']:
        return False
    elif text.lower() in ['true']:
        return True


def sort_dict_list(dict_to_sort: dict = None, sort_key='', reverse=False) -> list:
    sorted_list = sorted(dict_to_sort, key=operator.itemgetter(sort_key), reverse=reverse)
    return sorted_list


def get_local_suite_img_list(suite_path: str = None, format='jpg') -> list:
    """获取本地suite的图片列表"""
    if suite_path is None:
        return []
    # 复杂的路径glob匹配不了
    # img_file_list = glob.glob('{}/*.{}'.format(suite_path, format))
    files_list = os.listdir(suite_path)
    img_file_list = list(filter(lambda x: x.endswith(format), files_list))
    return img_file_list


def get_local_suite_count(suite_path: str = None) -> int:
    """本地suite图片数量"""
    return len(get_local_suite_img_list(suite_path))
