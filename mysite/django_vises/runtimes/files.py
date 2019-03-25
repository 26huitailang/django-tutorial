# coding: utf-8

import re
import logging

logger = logging.getLogger(__name__)


def rename_file_or_folder_name(name: str) -> str:
    """替换路径或文件中的非法字符"""
    new_name = re.sub(r'[/\\:*?"<>|&]', '-', name)  # 非法文件夹名字符
    if new_name != name:
        logger.info("name: {} | new: {}".format(name, new_name))
    return new_name
