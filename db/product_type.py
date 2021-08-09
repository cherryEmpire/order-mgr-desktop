# @Time   : 2021/8/7 4:32
# @Author   : 翁鑫豪
# @Description   : product_type.py
import sqlite3

from utils.constants import DB_NAME
from utils.system_util import get_abs_path


class ProductType:
    """连接数据库 获取cursor"""

    def __init__(self):
        self.conn = sqlite3.connect(get_abs_path(DB_NAME))
        self.cur = self.conn.cursor()

    def insert_product_type(self, type_name, type_no, type_desc):
        self.cur.execute("""INSERT INTO product_type
                    (type_name, type_no,type_desc) VALUES (?,?,?)""", (type_name, type_no, type_desc))
        self.commit()
        row_id = self.cur.execute("SELECT last_insert_rowid() from product_type")
        return row_id.lastrowid

    def update_product_type(self, type_id, type_name, type_no, type_desc):
        self.cur.execute("""UPDATE product_type
                     SET type_name=?, type_no=?,type_desc=? WHERE id=?""", [type_name, type_no, type_desc, type_id])
        self.commit()

    def delete_product_type(self, id):
        self.cur.execute("DELETE FROM product_type where id = ?", [id])
        self.commit()

    def query_product_type_by_id(self, id):
        result = []
        for row in self.cur.execute("SELECT id, type_name, type_no, type_desc FROM product_type where id = ?", [id]):
            result.append(row)
        return result

    def fetch_data(self):
        result = []
        for row in self.cur.execute("SELECT id, type_name, type_no, type_desc FROM product_type"):
            result.append(row)
        return result

    def commit(self):
        """commit提交"""
        self.cur.execute("commit")
