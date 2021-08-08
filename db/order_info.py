# @Time   : 2021/8/7 18:28
# @Author   : 翁鑫豪
# @Description   : order_info.py
import sqlite3

from utils.constants import DB_NAME
from utils.system_util import get_abs_path


class OrderInfo:
    """连接数据库 获取cursor"""

    def __init__(self):
        self.conn = sqlite3.connect(get_abs_path(DB_NAME))
        self.cur = self.conn.cursor()

    def insert_order_info(self, order_name, order_type_name, company_name, company_address, tel_no, phone_no, qq_no, order_desc):
        self.cur.execute("""INSERT INTO order_info
                    (order_name, order_type_name, company_name, company_address, tel_no, phone_no, qq_no, order_desc) VALUES (?,?,?,?,?,?,?,?)""", (order_name, order_type_name, company_name, company_address, tel_no, phone_no, qq_no, order_desc))
        self.commit()
        row_id = self.cur.execute("SELECT last_insert_rowid() from order_info")
        return row_id.lastrowid

    def delete_order_info(self, id):
        self.cur.execute("DELETE FROM order_info where id = ?", [id])
        self.commit()

    def query_order_info_by_id(self, id):
        result = []
        for row in self.cur.execute("SELECT id, order_name, order_type_name, company_name, company_address, tel_no, phone_no, qq_no, order_desc FROM order_info where id = ?", [id]):
            result.append(row)
        return result

    def fetch_data(self):
        result = []
        for row in self.cur.execute("SELECT id, order_name, order_type_name, company_name, company_address, tel_no, phone_no, qq_no, order_desc FROM order_info"):
            result.append(row)
        return result

    def commit(self):
        """commit提交"""
        self.cur.execute("commit")
