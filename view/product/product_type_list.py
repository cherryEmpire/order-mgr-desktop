# @Time   : 2021/8/7 3:32
# @Author   : 翁鑫豪
# @Description   : product_type_list.py
from PySide2.QtCore import Qt, Signal, QSize
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel, QHBoxLayout

from db.product_info import ProductInfo
from db.product_type import ProductType
from utils.constants import SYSTEM_FONT
from view.components.common_components import DeleteMessageBox
from view.components.list_item_widget import ListItemWidget
from view.components.new_add_dialog import NewAddDialog


class ProductTypeList(QWidget):
    signal_item_click = Signal(object)
    signal_item_remove = Signal(object)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setMargin(0)

        self.product_type_label = QLabel('商品大类')
        self.product_type_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        q_font = QFont(SYSTEM_FONT, 16)
        q_font.setBold(True)
        self.product_type_label.setFont(q_font)

        self.header_widget = QWidget(self)
        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setSpacing(0)
        self.header_layout.setMargin(0)

        self.add_product_type = QPushButton()
        self.add_product_type.clicked.connect(self.on_add_product_type_clicked)
        self.add_product_type.setIcon(QIcon(':/icon/icons/add.png'))

        self.remove_product_type = QPushButton()
        self.remove_product_type.clicked.connect(self.on_remove_product_type_clicked)
        self.remove_product_type.setIcon(QIcon(':/icon/icons/remove.png'))

        self.header_layout.addWidget(self.product_type_label, Qt.AlignVCenter | Qt.AlignHCenter)
        self.header_layout.addWidget(self.add_product_type, Qt.AlignRight | Qt.AlignHCenter)
        self.header_layout.addWidget(self.remove_product_type, Qt.AlignRight | Qt.AlignHCenter)

        self.main_layout.addWidget(self.header_widget)

        self.list = QListWidget(self)
        self.main_layout.addWidget(self.list)
        self.list.itemClicked.connect(self.on_list_item_click)
        self.load_data()

    def on_add_product_type_clicked(self):
        self.new_add = NewAddDialog()
        self.new_add.init_ui('新增商品大类', ['名称', '编号', '描述'])
        self.new_add.signal_ok.connect(self.add_new_product_type)
        self.new_add.show()

    def do_remove_product_type(self):
        item = self.list.currentItem()
        if item is None:
            return
        item_id = item.id
        product_type = ProductType()
        product_type.delete_product_type(item_id)
        product_info = ProductInfo()
        product_info.delete_product_info_by_type(item_id)
        self.list.takeItem(self.list.currentIndex().row())
        self.signal_item_remove.emit(self)

    def on_remove_product_type_clicked(self):
        self.delete_box = DeleteMessageBox(text='是否删除此商品大类？')
        self.delete_box.setWindowTitle('警告')
        self.delete_box.deleteBtn.clicked.connect(self.do_remove_product_type)
        self.delete_box.show()

    def add_new_product_type(self, keys, values):
        product_type = ProductType()
        id = product_type.insert_product_type(values[0], values[1], values[2])
        self.add_item(id, values[0], values[1], values[2])

    def update_product_type(self, keys, values):
        product_type = ProductType()
        item_widget = self.edit_form.item_widget
        product_type.update_product_type(item_widget.item.id, values[0], values[1], values[2])
        item_widget.label.setText(values[0])
        item_widget.item.type_name = values[0]
        item_widget.item.type_no = values[1]
        item_widget.item.type_desc = values[2]

    def load_data(self):
        product_type = ProductType()
        data = product_type.fetch_data()
        for row in data:
            self.add_item(row[0], row[1], row[2], row[3])

    def add_item(self, id, type_name, type_no, type_desc):
        item = QListWidgetItem()
        item.id = id
        item.type_name = type_name
        item.type_no = type_no
        item.type_desc = type_desc
        q_font = QFont(SYSTEM_FONT, 12)
        item.setFont(q_font)
        item.setSizeHint(QSize(100, 30))
        self.list.addItem(item)

        item_widget = ListItemWidget(self.list)
        item_widget.item = item
        item_widget.label.setText(type_name)
        item_widget.signal_edit_clicked.connect(self.on_edit_button_clicked)
        item_widget.signal_view_clicked.connect(self.on_view_button_clicked)
        self.list.setItemWidget(item, item_widget)

    def on_edit_button_clicked(self, item_widget):
        self.list.setItemSelected(item_widget.item, True)
        self.signal_item_click.emit(item_widget.item)
        self.edit_form = NewAddDialog()
        self.edit_form.item_widget = item_widget
        self.edit_form.init_ui(item_widget.item.type_name, ['名称', '编号', '描述'])
        self.edit_form.signal_ok.connect(self.update_product_type)
        item_id = item_widget.item.id
        product_type = ProductType()
        data = product_type.query_product_type_by_id(item_id)[0]
        self.edit_form.load_data(data[1:], 2)
        self.edit_form.show()

    def on_view_button_clicked(self, item_widget):
        self.list.setItemSelected(item_widget.item, True)
        self.signal_item_click.emit(item_widget.item)
        self.view_form = NewAddDialog()
        self.view_form.init_ui(item_widget.item.type_name, ['名称', '编号', '描述'])

        item_id = item_widget.item.id
        product_type = ProductType()
        data = product_type.query_product_type_by_id(item_id)[0]
        self.view_form.load_data(data[1:], 1)
        self.view_form.show()

    def on_list_item_click(self, *args, **kwargs):
        item: QListWidgetItem = args[0]
        self.signal_item_click.emit(item)
