# @Time   : 2021/8/6 22:03
# @Author   : 翁鑫豪
# @Description   : init_db.py

import sqlite3

from utils.constants import DB_NAME
from utils.system_util import get_abs_path


def system_init_db_step():
    """连接数据库"""
    conn = sqlite3.connect(get_abs_path(DB_NAME))
    sql_user_info_create = """create table if not exists user_info
    (
            id         INTEGER PRIMARY KEY,
            user_name       TEXT unique,
            full_name       TEXT,
            password        TEXT
    );"""
    sql_product_type_create = """create table if not exists product_type
    (
        id         INTEGER PRIMARY KEY,
        type_name    TEXT,
        type_no       TEXT,
        type_desc     TEXT
    );"""
    sql_product_info_create = """create table if not exists product_info
        (
            id         INTEGER PRIMARY KEY,
            product_type    INTEGER,
            product_name    TEXT,
            product_no       TEXT,
            product_price   TEXT,
            product_desc     TEXT
        );"""
    sql_order_info_create = """create table if not exists order_info
            (
                id         INTEGER PRIMARY KEY,
                order_name    TEXT,
                order_type_name TEXT,
                company_name       TEXT,
                company_address   TEXT,
                tel_no     TEXT,
                phone_no     TEXT,
                qq_no     TEXT,
                order_desc     TEXT
            );"""
    sql_order_sale_list_create = """create table if not exists order_sale_list
                (
                    id         INTEGER PRIMARY KEY,
                    order_id    INTEGER,
                    order_no    TEXT,
                    customer_company    TEXT,
                    customer_name    TEXT,
                    customer_phone    TEXT,
                    product_list    TEXT,
                    create_user       TEXT,
                    last_edit_user   TEXT,
                    create_date     TEXT,
                    last_edit_date     TEXT,
                    order_manager   TEXT,
                    goods_sender    TEXT,
                    goods_receiver   TEXT
                );"""
    """创建表格"""
    conn.execute(sql_user_info_create)
    conn.execute(sql_product_type_create)
    conn.execute(sql_product_info_create)
    conn.execute(sql_order_info_create)
    conn.execute(sql_order_sale_list_create)
    conn.close()
