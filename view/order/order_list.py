# @Time   : 2021/8/7 3:20
# @Author   : 翁鑫豪
# @Description   : order_list.py
from PySide2.QtCore import Qt, Signal, QSize
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QPushButton

from db.order_info import OrderInfo
from db.order_sale_list import OrderSaleList
from utils.constants import SYSTEM_FONT
from view.order.order_info_form import OrderInfoForm


class OrderList(QWidget):
    signal_item_click = Signal(object)
    signal_item_remove = Signal(object)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setMargin(0)

        self.order_list_label = QLabel('销售单据')
        self.order_list_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        q_font = QFont(SYSTEM_FONT, 16)
        q_font.setBold(True)
        self.order_list_label.setFont(q_font)

        self.header_widget = QWidget(self)
        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setSpacing(0)
        self.header_layout.setMargin(0)

        self.add_sale_order = QPushButton()
        self.add_sale_order.clicked.connect(self.on_add_sale_order_clicked)
        self.add_sale_order.setIcon(QIcon(':/icon/icons/add.png'))

        self.remove_sale_order = QPushButton()
        self.remove_sale_order.clicked.connect(self.on_remove_sale_order_clicked)
        self.remove_sale_order.setIcon(QIcon(':/icon/icons/remove.png'))

        self.header_layout.addWidget(self.order_list_label, Qt.AlignVCenter | Qt.AlignHCenter)
        self.header_layout.addWidget(self.add_sale_order, Qt.AlignRight | Qt.AlignHCenter)
        self.header_layout.addWidget(self.remove_sale_order, Qt.AlignRight | Qt.AlignHCenter)

        self.main_layout.addWidget(self.header_widget)

        self.list = QListWidget(self)
        self.main_layout.addWidget(self.list)
        self.list.itemClicked.connect(self.on_list_item_click)
        self.load_data()

    def on_add_sale_order_clicked(self):
        self.new_add = OrderInfoForm()
        self.new_add.init_ui()
        self.new_add.signal_ok.connect(self.add_new_order)
        self.new_add.show()

    def on_remove_sale_order_clicked(self):
        item = self.list.currentItem()
        if item is None:
            return
        item_id = item.id
        info = OrderInfo()
        info.delete_order_info(item_id)
        sale_list = OrderSaleList()
        sale_list.delete_order_sale_list_by_order_id(item_id)
        self.list.takeItem(self.list.currentIndex().row())
        self.signal_item_remove.emit(self)

    def add_new_order(self, keys, values):
        order_info = OrderInfo()
        id = order_info.insert_order_info(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])
        self.add_item(id, values[0], values[1])

    def load_data(self):
        order_info = OrderInfo()
        data = order_info.fetch_data()
        for row in data:
            self.add_item(row[0], row[1], row[2])

    def add_item(self, id, order_name, order_type):
        item = QListWidgetItem(order_name + order_type)
        item.id = id
        item.order_name = order_name
        item.order_type = order_type
        q_font = QFont(SYSTEM_FONT, 12)
        item.setFont(q_font)
        item.setSizeHint(QSize(100, 30))
        self.list.addItem(item)

    def on_list_item_click(self, *args, **kwargs):
        item: QListWidgetItem = args[0]
        self.signal_item_click.emit(item)
