# @Time   : 2021/8/6 22:14
# @Author   : 翁鑫豪
# @Description   : mainwindow_toolbar_controller.py

from PySide6.QtCore import QObject

from db.user_info import UserDto
from view.components.common_components import MessageBox


class MainWindowToolBarContext(QObject):

    def __init__(self, mainwindow, current_user) -> None:
        super().__init__()
        self.mainwindow = mainwindow
        self.current_user: UserDto = current_user

    def open_order(self):
        self.mainwindow.order_list.setVisible(True)
        count = self.mainwindow.order_list.list.count()
        if count == 0:
            self.mainwindow.order_list_item_table.setVisible(False)
        else:

            items = self.mainwindow.order_list.list.selectedItems()
            if items is None or len(items) == 0:
                self.mainwindow.order_list_item_table.setVisible(False)
            else:
                self.mainwindow.order_list_item_table.setVisible(True)
        self.mainwindow.product_type_list.setVisible(False)
        self.mainwindow.product_info_table.setVisible(False)

    def open_product(self):
        self.mainwindow.order_list.setVisible(False)
        self.mainwindow.order_list_item_table.setVisible(False)
        self.mainwindow.product_type_list.setVisible(True)
        count = self.mainwindow.product_type_list.list.count()
        if count == 0:
            self.mainwindow.product_info_table.setVisible(False)
        else:
            items = self.mainwindow.product_type_list.list.selectedItems()
            if items is None or len(items) == 0:
                self.mainwindow.product_info_table.setVisible(False)
            else:
                self.mainwindow.product_info_table.setVisible(True)

    def open_help(self):
        self.help_box = MessageBox(text='订单模板管理:可以新建模板\r\n订单管理:在模板中新建订单\r\n产品管理:管理产品信息，用于订单的中价格查询\r\n帮助\r\n关于')
        self.help_box.setWindowTitle("帮助")
        self.help_box.show()

    def open_about(self):
        self.about_box = MessageBox(text='销售单管理系统v1.0\r\nAuthor 一叶飘零Cherry')
        self.about_box.setWindowTitle("关于")
        self.about_box.show()

    def on_click_product_type_list_item(self, item):
        self.mainwindow.product_info_table.product_type_id = item.id
        self.mainwindow.product_info_table.product_type_name = item.type_name
        self.mainwindow.product_info_table.re_load_data()
        self.mainwindow.product_info_table.setVisible(True)

    def on_click_order_list_item(self, item):
        self.mainwindow.order_list_item_table.order_id = item.id
        self.mainwindow.order_list_item_table.order_name = item.order_name
        self.mainwindow.order_list_item_table.order_type = item.order_type
        self.mainwindow.order_list_item_table.current_user = self.current_user
        self.mainwindow.order_list_item_table.re_load_data()
        self.mainwindow.order_list_item_table.setVisible(True)

    def on_remove_order(self, obj):
        self.mainwindow.order_list_item_table.setVisible(False)

    def on_remove_product(self, obj):
        self.mainwindow.product_info_table.setVisible(False)
