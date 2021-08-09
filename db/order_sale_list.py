# @Time   : 2021/8/7 18:51
# @Author   : 翁鑫豪
# @Description   : order_sale_list.py
import json
import sqlite3
from datetime import datetime

from utils.constants import DB_NAME
from utils.system_util import get_abs_path


def to_float(text):
    if text == '':
        return 0
    return float(text)


class OrderSaleProductDto:

    def __init__(self) -> None:
        super().__init__()
        self.product_type_id = None
        self.product_info_id = None
        self.unit_desc = None
        self.count = None
        self.price = None
        self.desc = None

    def to_json(self):
        data = {}
        data["product_type_id"] = self.product_type_id
        data["product_info_id"] = self.product_info_id
        data["unit_desc"] = self.unit_desc
        data["price"] = self.price
        data["count"] = self.count
        data["desc"] = self.desc
        return data

    def load_json(self, data):
        self.product_type_id = data["product_type_id"]
        self.product_info_id = data["product_info_id"]
        self.unit_desc = data["unit_desc"]
        self.price = data["price"]
        self.count = data["count"]
        self.desc = data["desc"]


def product_list_tostr(product_dto_list):
    data = []
    if product_dto_list is not None:
        for item in product_dto_list:
            data.append(item.to_json())
    return json.dumps(data)


def load_product_list(product_dto_list_str):
    data_json = json.loads(product_dto_list_str)
    data = []
    for item in data_json:
        dto = OrderSaleProductDto()
        dto.load_json(item)
        data.append(dto)
    return data


class OrderSaleDto:

    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.order_id = None
        self.order_no = None
        self.customer_company = None
        self.customer_name = None
        self.customer_phone = None
        self.product_list: list(OrderSaleProductDto) = None
        self.create_user = None
        self.last_edit_user = None
        self.create_date = None
        self.last_edit_date = None
        self.order_manager = None
        self.goods_sender = None
        self.goods_receiver = None
        self.total_amount = None

    def load_data(self, data):
        self.id = data[0]
        self.order_id = data[1]
        self.order_no = data[2]
        self.customer_company = data[3]
        self.customer_name = data[4]
        self.customer_phone = data[5]
        self.product_list: list(OrderSaleProductDto) = load_product_list(data[6])
        self.create_user = data[7]
        self.last_edit_user = data[8]
        self.create_date = data[9]
        self.last_edit_date = data[10]
        self.order_manager = data[11]
        self.goods_sender = data[12]
        self.goods_receiver = data[13]
        self.total_amount = self.get_amount()

    def get_amount(self):
        amount = 0
        for item in self.product_list:
            amount += to_float(item.price) * to_float(item.count)
        return amount

    def get_count(self):
        count = 0
        for item in self.product_list:
            count += to_float(item.count)
        return count


class OrderSaleList:
    """连接数据库 获取cursor"""

    def __init__(self):
        self.conn = sqlite3.connect(get_abs_path(DB_NAME))
        self.cur = self.conn.cursor()

    def insert_order_sale_list(self, order_sale_dto: OrderSaleDto):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_sale_dto.create_date = now
        order_sale_dto.last_edit_date = now
        product_list = product_list_tostr(order_sale_dto.product_list)
        self.cur.execute("""INSERT INTO order_sale_list
                    (order_id, order_no, customer_company, customer_name, customer_phone, product_list, 
                    create_user, last_edit_user, create_date, last_edit_date, order_manager, goods_sender, goods_receiver) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                         (order_sale_dto.order_id, order_sale_dto.order_no, order_sale_dto.customer_company, order_sale_dto.customer_name, order_sale_dto.customer_phone,
                          product_list, order_sale_dto.create_user, order_sale_dto.last_edit_user, now, now, order_sale_dto.order_manager, order_sale_dto.goods_sender, order_sale_dto.goods_receiver))
        self.commit()
        row_id = self.cur.execute("SELECT last_insert_rowid() from order_sale_list")
        return row_id.lastrowid

    def update_order_sale_list(self, order_sale_dto: OrderSaleDto):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_sale_dto.last_edit_date = now
        product_list = product_list_tostr(order_sale_dto.product_list)
        self.cur.execute("""UPDATE order_sale_list
                    SET order_id=?, order_no=?, customer_company=?, customer_name=?, customer_phone=?, product_list=?, 
                    last_edit_user=?, last_edit_date=?, order_manager=?, goods_sender=?, goods_receiver=?""",
                         [order_sale_dto.order_id, order_sale_dto.order_no, order_sale_dto.customer_company, order_sale_dto.customer_name, order_sale_dto.customer_phone,
                          product_list, order_sale_dto.last_edit_user, now, order_sale_dto.order_manager, order_sale_dto.goods_sender, order_sale_dto.goods_receiver])
        self.commit()

    def delete_order_sale_list_by_id(self, id):
        self.cur.execute("DELETE FROM order_sale_list where id = ?", [id])
        self.commit()

    def delete_order_sale_list_by_no(self, order_no):
        self.cur.execute("DELETE FROM order_sale_list where order_no = ?", [order_no])
        self.commit()

    def query_order_sale_list_by_id(self, id):
        result = []
        for row in self.cur.execute("""SELECT id, order_id, order_no, customer_company, customer_name, customer_phone, product_list,
                    create_user, last_edit_user, create_date, last_edit_date, order_manager, goods_sender, goods_receiver FROM order_sale_list where id = ?""", [id]):
            dto = OrderSaleDto()
            dto.load_data(row)
            result.append(dto)
        return result

    def query_order_sale_list_by_no(self, order_no):
        result = []
        for row in self.cur.execute("""SELECT id, order_id, order_no, customer_company, customer_name, customer_phone, product_list,
                    create_user, last_edit_user, create_date, last_edit_date, order_manager, goods_sender, goods_receiver FROM order_sale_list where order_no = ?""", [order_no]):
            dto = OrderSaleDto()
            dto.load_data(row)
            result.append(dto)
        return result

    def fetch_data_by_order_id(self, order_id):
        result = []
        for row in self.cur.execute("""SELECT id, order_id, order_no, customer_company, customer_name, customer_phone, product_list,
                    create_user, last_edit_user, create_date, last_edit_date, order_manager, goods_sender, goods_receiver FROM order_sale_list where order_id = ?""", [order_id]):
            dto = OrderSaleDto()
            dto.load_data(row)
            result.append(dto)
        return result

    def fetch_count_by_order_id_date(self, order_id, date):
        result = []
        for row in self.cur.execute("""SELECT id, create_date FROM order_sale_list where order_id = ? and create_date like ?||'%'""", [order_id, date]):
            result.append(row)
        return len(result)

    def commit(self):
        """commit提交"""
        self.cur.execute("commit")
