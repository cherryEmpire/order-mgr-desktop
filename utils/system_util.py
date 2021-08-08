# @Time   : 2021/8/6 22:00
# @Author   : 翁鑫豪
# @Description   : system_util.py
from pathlib import Path

from utils.constants import HOME_PATH


def get_home_abs_path():
    """获取绝对路径"""
    path = Path.home().joinpath(HOME_PATH)
    return path


def get_abs_path(path_):
    return Path.joinpath(get_home_abs_path(), path_)
