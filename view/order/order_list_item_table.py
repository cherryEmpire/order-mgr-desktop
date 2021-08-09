# @Time   : 2021/8/7 3:20
# @Author   : 翁鑫豪
# @Description   : order_list_item_table.py

from PySide2.QtCore import QRegExp, Qt, QSize
from PySide2.QtGui import QIcon, QRegExpValidator, QCursor
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QStyleFactory, QHeaderView, QAbstractItemView, QTableWidgetItem, QMenu, QAction

from db.order_sale_list import OrderSaleList, OrderSaleDto
from db.user_info import UserDto
from view.components.common_components import ReadOnlyDelegate, DeleteMessageBox
from view.order.order_item_form import OrderDetailForm


class OrderListItemTable(QWidget):

    def init_ui(self):
        self.current_user: UserDto = None
        self.order_id = None
        self.order_name = None
        self.order_type = None
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setMargin(0)
        self.main_layout.setSpacing(0)
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        horizontal_header = self.table.horizontalHeader()
        horizontal_header.setObjectName("productinfo_table_header")
        horizontal_header.setStyle(QStyleFactory.create("Fusion"))
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setHighlightSections(False)
        delegate = ReadOnlyDelegate()
        self.table.setItemDelegateForColumn(0, delegate)
        self.table.setItemDelegateForColumn(1, delegate)
        self.table.setItemDelegateForColumn(2, delegate)
        self.table.setItemDelegateForColumn(3, delegate)
        self.table.setItemDelegateForColumn(4, delegate)
        self.table.setItemDelegateForColumn(5, delegate)
        self.table.setItemDelegateForColumn(6, delegate)
        # self.table.cellDoubleClicked.connect(self.on_click_cell)
        horizontal_header.setSectionResizeMode(0, QHeaderView.Fixed)
        horizontal_header.setSectionResizeMode(1, QHeaderView.Fixed)
        horizontal_header.setSectionResizeMode(2, QHeaderView.Stretch)
        horizontal_header.setSectionResizeMode(3, QHeaderView.Fixed)
        horizontal_header.setSectionResizeMode(4, QHeaderView.Fixed)
        horizontal_header.setSectionResizeMode(5, QHeaderView.Stretch)
        horizontal_header.setSectionResizeMode(6, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 150)

        self.main_layout.addWidget(self.table)

        self.add_order_detail = QPushButton()
        self.add_order_detail.clicked.connect(self.on_add_order_detail_clicked)
        self.add_order_detail.setIcon(QIcon(':/icon/icons/add.png'))
        self.add_order_detail.setFixedHeight(40)

        self.main_layout.addWidget(self.add_order_detail)
        self.reg_exp = QRegExp("^(-?\d+)(\.\d+)?$")
        self.reg_exp_validator = QRegExpValidator(self.reg_exp, self)

    def on_add_order_detail_clicked(self):
        self.new_add = OrderDetailForm()
        self.new_add.init_ui(self.current_user, self.order_id, True)
        self.new_add.signal_ok.connect(self.add_new_order_detail)
        self.new_add.show()

    def add_new_order_detail(self, keys, data: OrderSaleDto):
        order_sale_list = OrderSaleList()
        sale_id = order_sale_list.insert_order_sale_list(data)
        data.id = sale_id
        self.add_row(data)

    def update_order_detail(self, keys, data: OrderSaleDto):
        row_index = self.table.currentIndex().row()
        order_sale_list = OrderSaleList()
        data.last_edit_user = self.current_user.full_name
        order_sale_list.update_order_sale_list(data)
        self.update_row(row_index, data)

    def update_row(self, row_index, data: OrderSaleDto):
        self.table.item(row_index, 2).setText(str(data.get_amount()))
        self.table.item(row_index, 4).setText(data.last_edit_date)

    def add_row(self, detail_dto: OrderSaleDto):
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        index_cell = QTableWidgetItem(str(row_index + 1))
        index_cell.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_index, 0, index_cell)

        order_no_cell = QTableWidgetItem(detail_dto.order_no)
        order_no_cell.order_info = detail_dto
        order_no_cell.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_index, 1, order_no_cell)

        amount_cell = QTableWidgetItem(str(detail_dto.get_amount()))
        amount_cell.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.table.setItem(row_index, 2, amount_cell)

        create_date_cell = QTableWidgetItem(detail_dto.create_date)
        create_date_cell.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_index, 3, create_date_cell)

        last_edit_cell = QTableWidgetItem(detail_dto.last_edit_date)
        last_edit_cell.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_index, 4, last_edit_cell)

        create_user_cell = QTableWidgetItem(detail_dto.create_user)
        create_user_cell.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_index, 5, create_user_cell)

        operate_button = QPushButton()
        operate_button.setIcon(QIcon(':/icon/icons/operate_button.png'))
        operate_button.setIconSize(QSize(16, 16))
        operate_button.setObjectName("table_operate_button")
        operate_button.clicked.connect(self.__click_operate_button)
        self.table.setCellWidget(row_index, 6, operate_button)

    def load_data(self):
        self.headers = ['序号', self.order_type + '编号', '总金额', '创建日期', '最后修改日期', '经办人', '操作']
        self.table.setHorizontalHeaderLabels(self.headers)
        order_sale_list = OrderSaleList()
        data = order_sale_list.fetch_data_by_order_id(self.order_id)
        for row in data:
            self.add_row(row)

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

        menu_action_export = QAction(QIcon(':/icon/icons/menu/export.png'), '导出', self.menu)
        menu_action_export.triggered.connect(self.on_click_menu_export)
        self.menu.addAction(menu_action_export)

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
        order_info: OrderSaleDto = self.table.item(row_index, 1).order_info
        self.view_form = OrderDetailForm()
        self.view_form.init_ui(self.current_user, self.order_id, False)
        self.view_form.load_data(order_info.id, order_info.order_no, 1)
        self.view_form.signal_ok.connect(self.on_click_menu_cancel)
        self.view_form.show()

    def on_click_menu_edit(self):
        row_index = self.table.currentIndex().row()
        order_info: OrderSaleDto = self.table.item(row_index, 1).order_info
        self.view_form = OrderDetailForm()
        self.view_form.init_ui(self.current_user, self.order_id, False)
        self.view_form.load_data(order_info.id, order_info.order_no, 2)
        self.view_form.signal_ok.connect(self.update_order_detail)
        self.view_form.show()

    def on_click_menu_export(self):
        row_index = self.table.currentIndex().row()
        order_info: OrderSaleDto = self.table.item(row_index, 1).order_info
        order_sale_list = OrderSaleList()
        sale_list = order_sale_list.query_order_sale_list_by_id(order_info.id)
        list_ = sale_list[0]
        # self.new_add = OrderDetailForm()
        # self.new_add.init_ui(self.current_user, self.order_id, True)
        # self.new_add.signal_ok.connect(self.add_new_order_detail)
        # self.new_add.show()
        pass

    def on_click_menu_delete(self):
        self.delete_box = DeleteMessageBox(text='是否删除此单据？')
        self.delete_box.setWindowTitle('警告')
        self.delete_box.deleteBtn.clicked.connect(self.do_delete)
        self.delete_box.show()

    def do_delete(self):
        row_index = self.table.currentIndex().row()
        order_info: OrderSaleDto = self.table.item(row_index, 1).order_info
        order_sale_list = OrderSaleList()
        order_sale_list.delete_order_sale_list_by_id(order_info.id)
        self.table.removeRow(row_index)
        self.refresh_index()

    def on_click_menu_cancel(self):
        pass

    def refresh_index(self):
        count = self.table.rowCount()
        for i in range(count):
            self.table.item(i, 0).setText(str(i + 1))
