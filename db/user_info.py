# @Time   : 2021/8/7 0:23
# @Author   : 翁鑫豪
# @Description   : user_info.py
import sqlite3

from utils.constants import DB_NAME
from utils.system_util import get_abs_path


class UserDto:

    def __init__(self, user_name, full_name, user_type) -> None:
        super().__init__()
        self.user_name = user_name
        self.full_name = full_name
        self.type = user_type


class UserInfo:
    """连接数据库 获取cursor"""

    def __init__(self):
        self.conn = sqlite3.connect(get_abs_path(DB_NAME))
        self.cur = self.conn.cursor()

    def insert_user_info(self, user_name, full_name, password):
        self.cur.execute("""INSERT INTO user_info
                    (user_name, full_name, password) VALUES (?,?,?)""",
                         (user_name, full_name, password))
        self.commit()

    def delete_user(self, user_name):
        self.cur.execute("DELETE FROM user_info where user_name = ?", [user_name])
        self.commit()

    def query_user_by_name(self, user_name):
        result = []
        for row in self.cur.execute("SELECT user_name, full_name, password FROM user_info where user_name = ?", [user_name]):
            result.append(row)
        return result

    def user_exist(self, user_name):
        result = self.query_user_by_name(user_name)
        if result is None or len(result) == 0:
            return False
        return True

    def commit(self):
        """commit提交"""
        self.cur.execute("commit")
