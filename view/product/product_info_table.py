# @Time   : 2021/8/7 15:45
# @Author   : 翁鑫豪
# @Description   : product_info_table.py

from PySide2.QtCore import QRegExp, Qt, QSize
from PySide2.QtGui import QIcon, QRegExpValidator, QCursor
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QStyleFactory, QHeaderView, QAbstractItemView, QLineEdit, QTableWidgetItem, QMenu, QAction

from db.product_info import ProductInfo
from view.components.common_components import ReadOnlyDelegate, DeleteMessageBox
from view.components.new_add_dialog import NewAddDialog


class ProductInfoTable(QWidget):

    def init_ui(self):
        self.product_type_id = None
        self.product_type_name = None
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setMargin(0)
        self.main_layout.setSpacing(0)
        self.table = QTableWidget(self)

        self.table.setColumnCount(6)
        horizontal_header = self.table.horizontalHeader()
        horizontal_header.setObjectName("productinfo_table_header")
        horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
        horizontal_header.setStyle(QStyleFactory.create("Fusion"))
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.keys = ['商品名称', '商品编号', '单价', '备注']
        self.headers = ['序号']
        self.headers.extend(self.keys)
        self.headers.append('操作')
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.horizontalHeader().setHighlightSections(False)
        delegate = ReadOnlyDelegate()
        self.table.setItemDelegateForColumn(0, delegate)
        self.table.setItemDelegateForColumn(1, delegate)
        self.table.setItemDelegateForColumn(2, delegate)
        self.table.setItemDelegateForColumn(3, delegate)
        self.table.setItemDelegateForColumn(4, delegate)
        self.table.setItemDelegateForColumn(5, delegate)
        # self.table.cellDoubleClicked.connect(self.on_click_cell)

        self.main_layout.addWidget(self.table)

        self.add_product_info = QPushButton()
        self.add_product_info.clicked.connect(self.on_add_product_info_clicked)
        self.add_product_info.setIcon(QIcon(':/icon/icons/add.png'))
        self.add_product_info.setFixedHeight(40)

        self.main_layout.addWidget(self.add_product_info)
        self.reg_exp = QRegExp("^(-?\d+)(\.\d+)?$")
        self.reg_exp_validator = QRegExpValidator(self.reg_exp, self)

    def on_add_product_info_clicked(self):
        self.new_add = NewAddDialog()
        self.new_add.init_ui('新增商品项', self.keys)
        price_edit: QLineEdit = self.new_add.edit_list[2]
        price_edit.setValidator(self.reg_exp_validator)
        self.new_add.signal_ok.connect(self.add_new_product_info)
        self.new_add.show()

    def add_new_product_info(self, keys, data):
        product_info = ProductInfo()
        product_info_id = product_info.insert_product_info(self.product_type_id, data[0], data[1], data[2], data[3])
        self.add_row(product_info_id, data[0], data[1], data[2], data[3])

    def add_row(self, id, product_name, product_no, product_price, product_desc):
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        index_cell = QTableWidgetItem(str(row_index + 1))
        index_cell.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_index, 0, index_cell)

        product_name_cell = QTableWidgetItem(product_name)
        product_name_cell.product_info_id = id
        product_name_cell.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_index, 1, product_name_cell)

        product_no_cell = QTableWidgetItem(product_no)
        product_no_cell.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_index, 2, product_no_cell)

        product_price_cell = QTableWidgetItem(product_price)
        product_price_cell.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.table.setItem(row_index, 3, product_price_cell)

        product_desc_cell = QTableWidgetItem(product_desc)
        product_desc_cell.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_index, 4, product_desc_cell)

        operate_button = QPushButton()
        operate_button.setIcon(QIcon(':/icon/icons/operate_button.png'))
        operate_button.setIconSize(QSize(16, 16))
        operate_button.setObjectName("table_operate_button")
        operate_button.clicked.connect(self.__click_operate_button)
        self.table.setCellWidget(row_index, 5, operate_button)

    def load_data(self):
        product_info = ProductInfo()
        data = product_info.fetch_data_by_product_type(self.product_type_id)
        for row in data:
            self.add_row(row[0], row[2], row[3], row[4], row[5])

    def re_load_data(self):
        self.clear_data()
        self.load_data()

    def clear_data(self):
        row_count = self.table.rowCount()
        for i in range(row_count):
            self.table.removeRow(0)

    def __click_operate_button(self, *args, **kwargs):
        self.menu = QMenu()

        menu_action_open = QAction(QIcon(':/icon/icons/menu/open.png'), '查看', self.menu)
        menu_action_open.triggered.connect(self.on_click_menu_view)
        self.menu.addAction(menu_action_open)

        menu_action_copy_open = QAction(QIcon(':/icon/icons/menu/edit.png'), '编辑', self.menu)
        menu_action_copy_open.triggered.connect(self.on_click_menu_edit)
        self.menu.addAction(menu_action_copy_open)

        menu_action_delete = QAction(QIcon(':/icon/icons/menu/delete.png'), '删除', self.menu)
        menu_action_delete.triggered.connect(self.on_click_menu_delete)
        self.menu.addAction(menu_action_delete)

        self.menu.addSeparator()

        menu_action_cancel = QAction(QIcon(':/icon/icons/menu/cancel.png'), '取消', self.menu)
        menu_action_cancel.triggered.connect(self.on_click_menu_cancel)
        self.menu.addAction(menu_action_cancel)

        self.menu.exec_(QCursor.pos())

    def on_click_menu_view(self):
        row_index = self.table.currentIndex().row()
        item = self.table.item(row_index, 1)
        info_id = item.product_info_id
        product_info = ProductInfo()
        data = product_info.query_product_info_by_id(info_id)[0]
        self.view_form = NewAddDialog()
        self.view_form.init_ui(data[2], self.keys)
        self.view_form.load_data(data[2:], 1)
        self.view_form.signal_ok.connect(self.on_click_menu_cancel)
        self.view_form.show()

    def on_click_menu_edit(self):
        row_index = self.table.currentIndex().row()
        item = self.table.item(row_index, 1)
        info_id = item.product_info_id
        product_info = ProductInfo()
        data = product_info.query_product_info_by_id(info_id)[0]
        self.edit_form = NewAddDialog()
        self.edit_form.init_ui(data[2], self.keys)
        price_edit: QLineEdit = self.edit_form.edit_list[2]
        price_edit.setValidator(self.reg_exp_validator)
        self.edit_form.load_data(data[2:], 2)
        self.edit_form.signal_ok.connect(self.on_update_product_info)
        self.edit_form.show()

    def on_click_menu_delete(self):
        self.delete_box = DeleteMessageBox(text='是否删除此产品信息？')
        self.delete_box.setWindowTitle('警告')
        self.delete_box.deleteBtn.clicked.connect(self.do_delete)
        self.delete_box.show()

    def do_delete(self):
        row_index = self.table.currentIndex().row()
        item = self.table.item(row_index, 1)
        info_id = item.product_info_id
        product_info = ProductInfo()
        product_info.delete_product_info(info_id)
        self.table.removeRow(row_index)
        self.refresh_index()

    def on_click_menu_cancel(self):
        pass

    def on_update_product_info(self, keys, data):
        row_index = self.table.currentIndex().row()
        item = self.table.item(row_index, 1)
        info_id = item.product_info_id
        product_info = ProductInfo()
        product_info.update_product_info(info_id, self.product_type_id, data[0], data[1], data[2], data[3])
        self.update_row(row_index, data)

    def update_row(self, row_index, data):
        self.table.item(row_index, 1).setText(data[0])
        self.table.item(row_index, 2).setText(data[1])
        self.table.item(row_index, 3).setText(data[2])
        self.table.item(row_index, 4).setText(data[3])

    def refresh_index(self):
        count = self.table.rowCount()
        for i in range(count):
            self.table.item(i, 0).setText(str(i + 1))
