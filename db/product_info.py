# @Time   : 2021/8/7 16:17
# @Author   : 翁鑫豪
# @Description   : product_info.py
import sqlite3

from utils.constants import DB_NAME
from utils.system_util import get_abs_path


class ProductInfo:
    """连接数据库 获取cursor"""

    def __init__(self):
        self.conn = sqlite3.connect(get_abs_path(DB_NAME))
        self.cur = self.conn.cursor()

    def insert_product_info(self, product_type, product_name, product_no, product_price, product_desc):
        self.cur.execute("""INSERT INTO product_info
                    (product_type, product_name, product_no, product_price, product_desc) VALUES (?,?,?,?,?)""", (product_type, product_name, product_no, product_price, product_desc))
        self.commit()
        row_id = self.cur.execute("SELECT last_insert_rowid() from product_info")
        return row_id.lastrowid

    def update_product_info(self, product_id, product_type, product_name, product_no, product_price, product_desc):
        self.cur.execute("""UPDATE product_info
                            SET product_type=?, product_name=?, product_no=?, product_price=?, product_desc=? where id=?""",
                         [product_type, product_name, product_no, product_price, product_desc, product_id])
        self.commit()

    def delete_product_info(self, id):
        self.cur.execute("DELETE FROM product_info where id = ?", [id])
        self.commit()

    def delete_product_info_by_type(self, product_type):
        self.cur.execute("DELETE FROM product_info where product_type = ?", [product_type])
        self.commit()

    def query_product_info_by_id(self, id):
        result = []
        for row in self.cur.execute("SELECT id, product_type, product_name, product_no, product_price, product_desc FROM product_info where id = ?", [id]):
            result.append(row)
        return result

    def fetch_data_by_product_type(self, product_type):
        result = []
        for row in self.cur.execute("SELECT id, product_type, product_name, product_no, product_price, product_desc FROM product_info where product_type = ?", [product_type]):
            result.append(row)
        return result

    def commit(self):
        """commit提交"""
        self.cur.execute("commit")
