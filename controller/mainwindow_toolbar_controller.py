# @Time   : 2021/8/6 22:14
# @Author   : 翁鑫豪
# @Description   : mainwindow_toolbar_controller.py

from PySide2.QtCore import QObject

from db.user_info import UserDto


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
        pass

    def open_about(self):
        pass

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
