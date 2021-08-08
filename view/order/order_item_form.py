# @Time   : 2021/8/7 17:33
# @Author   : 翁鑫豪
# @Description   : order_item_form.py
from datetime import datetime

from PySide2.QtCore import Qt, Signal, QRegExp
from PySide2.QtGui import QIcon, QFont, QRegExpValidator
from PySide2.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
    QLabel, QTableWidget, QTableWidgetItem, QWidget, QAbstractItemView, QHeaderView, QStyleFactory, QSizePolicy, QScrollBar, QTreeWidgetItem

from db.order_info import OrderInfo
from db.order_sale_list import OrderSaleList, OrderSaleDto, OrderSaleProductDto
from db.user_info import UserDto
from utils.common_util import get_chinese_all_upper, num2money_format
from utils.constants import HEADER_FONT
from view.components.cell_edit import CellLineEdit
from view.components.common_components import ReadOnlyDelegate
from view.components.tree_combobox import TreeComboBox


class OrderDetailForm(QDialog):
    signal_ok = Signal(object, object)

    def init_ui(self, current_user, order_id, new_add: bool):
        self.new_add = new_add
        self.order_id = order_id
        self.detail_id = None
        self.current_user: UserDto = current_user

        self.reg_exp = QRegExp("^(-?\d+)(\.\d+)?$")
        self.reg_exp_validator = QRegExpValidator(self.reg_exp, self)
        self.setWindowTitle('')
        self.setMinimumSize(1280, 720)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(':/icon/icons/main.png'))
        self.main_layout = QVBoxLayout(self)

        self.header = QLabel('', self)
        q_font = QFont(HEADER_FONT, 30)
        q_font.setBold(True)
        self.header.setFont(q_font)
        self.header.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.header)

        self.header_detail_layout = QHBoxLayout(self)
        self.header_detail_layout.setMargin(0)
        self.header_detail_layout.setSpacing(5)
        self.header_label1 = QLabel('购买单位:', self)
        self.header_label2 = QLineEdit(self)
        self.header_label3 = QLabel('客户:', self)
        self.header_label4 = QLineEdit(self)
        self.header_label5 = QLabel('联系电话:', self)
        self.header_label6 = QLineEdit(self)
        self.header_label7 = QLabel('单据编号:', self)
        self.header_label8 = QLabel('', self)
        self.header_detail_layout.addWidget(self.header_label1, 1, alignment=Qt.AlignRight)
        self.header_detail_layout.addWidget(self.header_label2, 4, alignment=Qt.AlignLeft)
        self.header_detail_layout.addWidget(self.header_label3, 1, alignment=Qt.AlignRight)
        self.header_detail_layout.addWidget(self.header_label4, 4, alignment=Qt.AlignLeft)
        self.header_detail_layout.addWidget(self.header_label5, 1, alignment=Qt.AlignRight)
        self.header_detail_layout.addWidget(self.header_label6, 4, alignment=Qt.AlignLeft)
        self.header_detail_layout.addWidget(self.header_label7, 1, alignment=Qt.AlignRight)
        self.header_detail_layout.addWidget(self.header_label8, 4, alignment=Qt.AlignLeft)
        self.main_layout.addLayout(self.header_detail_layout)

        self.init_table()

        self.tail_detail_layout_row1 = QHBoxLayout(self)
        self.tail_row1_label1 = QLabel('地址:', self)
        self.tail_row1_label2 = QLabel('', self)
        self.tail_row1_label3 = QLabel('电话:', self)
        self.tail_row1_label4 = QLabel('', self)
        self.tail_row1_label5 = QLabel('', self)
        self.tail_row1_label6 = QLabel('QQ:', self)
        self.tail_row1_label7 = QLabel('', self)
        self.tail_detail_layout_row1.addWidget(self.tail_row1_label1, 1, alignment=Qt.AlignRight)
        self.tail_detail_layout_row1.addWidget(self.tail_row1_label2, 4, alignment=Qt.AlignLeft)
        self.tail_detail_layout_row1.addWidget(self.tail_row1_label3, 1, alignment=Qt.AlignRight)
        self.tail_detail_layout_row1.addWidget(self.tail_row1_label4, 4, alignment=Qt.AlignLeft)
        self.tail_detail_layout_row1.addWidget(self.tail_row1_label5, 5, alignment=Qt.AlignLeft)
        self.tail_detail_layout_row1.addWidget(self.tail_row1_label6, 1, alignment=Qt.AlignRight)
        self.tail_detail_layout_row1.addWidget(self.tail_row1_label7, 4, alignment=Qt.AlignLeft)
        self.main_layout.addLayout(self.tail_detail_layout_row1)

        self.tail_detail_layout_row2 = QHBoxLayout(self)
        self.tail_row2_label1 = QLabel('备注:', self)
        self.tail_row2_label2 = QLabel('', self)
        self.tail_row2_label2.setAlignment(Qt.AlignLeft)
        self.tail_detail_layout_row2.addWidget(self.tail_row2_label1, 1, alignment=Qt.AlignRight)
        self.tail_detail_layout_row2.addWidget(self.tail_row2_label2, 19, alignment=Qt.AlignLeft)
        self.main_layout.addLayout(self.tail_detail_layout_row2)

        self.tail_detail_layout_row3 = QHBoxLayout(self)
        self.tail_row3_label1 = QLabel('开单人:', self)
        self.tail_row3_label2 = QLineEdit(self)
        self.tail_row3_label3 = QLabel('经手人:', self)
        self.tail_row3_label4 = QLineEdit(self)
        self.tail_row3_label5 = QLabel('送货人:', self)
        self.tail_row3_label6 = QLineEdit(self)
        self.tail_row3_label7 = QLabel('收货人:', self)
        self.tail_row3_label8 = QLineEdit(self)
        self.tail_detail_layout_row3.addWidget(self.tail_row3_label1, 1, alignment=Qt.AlignRight)
        self.tail_detail_layout_row3.addWidget(self.tail_row3_label2, 4, alignment=Qt.AlignLeft)
        self.tail_detail_layout_row3.addWidget(self.tail_row3_label3, 1, alignment=Qt.AlignRight)
        self.tail_detail_layout_row3.addWidget(self.tail_row3_label4, 4, alignment=Qt.AlignLeft)
        self.tail_detail_layout_row3.addWidget(self.tail_row3_label5, 1, alignment=Qt.AlignRight)
        self.tail_detail_layout_row3.addWidget(self.tail_row3_label6, 4, alignment=Qt.AlignLeft)
        self.tail_detail_layout_row3.addWidget(self.tail_row3_label7, 1, alignment=Qt.AlignRight)
        self.tail_detail_layout_row3.addWidget(self.tail_row3_label8, 4, alignment=Qt.AlignLeft)
        self.main_layout.addLayout(self.tail_detail_layout_row3)

        self.button_layout = QHBoxLayout(self)
        self.button_ok = QPushButton('确定')
        self.button_ok.clicked.connect(self.onclick_ok)
        self.button_cancel = QPushButton('取消')
        self.button_cancel.clicked.connect(self.onclick_cancel)
        self.button_layout.addWidget(self.button_ok)
        self.button_layout.addWidget(self.button_cancel)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.init_data()

    def init_table(self):
        self.table_view = QWidget(self)
        self.table_view_main_layout = QHBoxLayout(self.table_view)
        self.table_view_main_layout.setSpacing(0)
        self.table_view_main_layout.setMargin(0)
        self.table_view_layout = QVBoxLayout()
        self.table_view_layout.setSpacing(0)
        self.table_view_layout.setMargin(0)
        self.select_row = None
        self.table = QTableWidget(self.table_view)
        self.table.setColumnCount(7)
        horizontal_header = self.table.horizontalHeader()
        self.table.setHorizontalHeaderLabels(['No.', '商品名称', '单位', '数量', '单价', '金额', '备注'])
        # horizontal_header.setObjectName("productinfo_table_header")
        # horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
        horizontal_header.setSectionResizeMode(0, QHeaderView.Fixed)
        horizontal_header.setSectionResizeMode(1, QHeaderView.Fixed)
        horizontal_header.setSectionResizeMode(2, QHeaderView.Stretch)
        horizontal_header.setSectionResizeMode(3, QHeaderView.Stretch)
        horizontal_header.setSectionResizeMode(4, QHeaderView.Stretch)
        horizontal_header.setSectionResizeMode(5, QHeaderView.Stretch)
        horizontal_header.setSectionResizeMode(6, QHeaderView.Fixed)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 400)
        self.table.setColumnWidth(6, 250)
        horizontal_header.setStyle(QStyleFactory.create("Fusion"))
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setHighlightSections(False)
        delegate = ReadOnlyDelegate()
        self.table.setItemDelegateForColumn(0, delegate)
        self.table.setItemDelegateForColumn(5, delegate)
        self.table.itemClicked.connect(self.on_cell_clicked)
        # self.table.setItemDelegateForColumn(1, delegate)
        # self.table.setItemDelegateForColumn(2, delegate)
        # self.table.setItemDelegateForColumn(3, delegate)
        # self.table.setItemDelegateForColumn(4, delegate)
        # self.table.setItemDelegateForColumn(5, delegate)
        # self.table.setItemDelegateForColumn(6, delegate)
        self.table_view_layout.addWidget(self.table)

        self.amount_table = QTableWidget(self.table_view)
        amount_horizontal_header = self.amount_table.horizontalHeader()
        self.amount_table.setMaximumHeight(30)
        self.amount_table.setColumnCount(7)
        amount_horizontal_header.setSectionResizeMode(0, QHeaderView.Fixed)
        amount_horizontal_header.setSectionResizeMode(1, QHeaderView.Fixed)
        amount_horizontal_header.setSectionResizeMode(2, QHeaderView.Stretch)
        amount_horizontal_header.setSectionResizeMode(3, QHeaderView.Stretch)
        amount_horizontal_header.setSectionResizeMode(4, QHeaderView.Stretch)
        amount_horizontal_header.setSectionResizeMode(5, QHeaderView.Stretch)
        amount_horizontal_header.setSectionResizeMode(6, QHeaderView.Fixed)
        self.amount_table.setColumnWidth(0, 80)
        self.amount_table.setColumnWidth(1, 400)
        self.amount_table.setColumnWidth(6, 400)
        self.amount_table.setItemDelegateForColumn(0, delegate)
        self.amount_table.setItemDelegateForColumn(1, delegate)
        self.amount_table.setItemDelegateForColumn(2, delegate)
        self.amount_table.setItemDelegateForColumn(3, delegate)
        self.amount_table.setItemDelegateForColumn(4, delegate)
        self.amount_table.setItemDelegateForColumn(5, delegate)
        self.amount_table.setItemDelegateForColumn(6, delegate)
        self.amount_table.verticalHeader().setVisible(False)
        self.amount_table.horizontalHeader().setVisible(False)
        self.table_view_layout.addWidget(self.amount_table)
        self.amount_table.insertRow(0)

        item1 = QTableWidgetItem('合计(大写):')
        item1.setTextAlignment(Qt.AlignCenter)
        item1.setFlags(Qt.ItemIsEnabled)
        self.amount_table.setItem(0, 0, item1)

        self.total_cell_cn = QTableWidgetItem('')
        self.total_cell_cn.setFlags(Qt.ItemIsEnabled)
        self.total_cell_cn.setTextAlignment(Qt.AlignCenter)
        self.amount_table.setItem(0, 1, self.total_cell_cn)
        self.amount_table.setSpan(0, 1, 1, 2)

        self.total_cell_count = QTableWidgetItem('')
        self.total_cell_count.setFlags(Qt.ItemIsEnabled)
        self.total_cell_count.setTextAlignment(Qt.AlignCenter)
        self.amount_table.setItem(0, 3, self.total_cell_count)

        item4 = QTableWidgetItem('合计(小写):')
        item4.setFlags(Qt.ItemIsEnabled)
        item4.setTextAlignment(Qt.AlignCenter)
        self.amount_table.setItem(0, 4, item4)

        self.total_cell_num = QTableWidgetItem('')
        self.total_cell_num.setFlags(Qt.ItemIsEnabled)
        self.total_cell_num.setTextAlignment(Qt.AlignCenter)
        self.amount_table.setItem(0, 5, self.total_cell_num)
        self.amount_table.setSpan(0, 5, 1, 2)

        self.scrollbar = QScrollBar()
        self.scrollbar.setRange(0, 0)
        self.scrollbar.valueChanged.connect(self.on_scrollbar_value_change)

        self.table_view_button_layout = QVBoxLayout()
        self.table_view_button_layout.setSpacing(0)
        self.table_view_button_layout.setMargin(0)
        self.add_button = QPushButton()
        self.add_button.setIcon(QIcon(':/icon/icons/add.png'))
        self.remove_button = QPushButton()
        self.remove_button.setIcon(QIcon(':/icon/icons/remove.png'))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.add_button.setSizePolicy(sizePolicy)
        self.remove_button.setSizePolicy(sizePolicy)
        self.table_view_button_layout.addWidget(self.add_button, 1)
        self.table_view_button_layout.addWidget(self.remove_button, 1)
        self.add_button.clicked.connect(self.add_row)
        self.remove_button.clicked.connect(self.remove_row)

        self.table_view_main_layout.addLayout(self.table_view_layout)
        self.table_view_main_layout.addWidget(self.scrollbar)
        self.table_view_main_layout.addLayout(self.table_view_button_layout)
        self.main_layout.addWidget(self.table_view)

    def onclick_ok(self):
        dto = OrderSaleDto()
        dto.id = self.detail_id
        dto.order_id = self.order_id
        dto.order_no = self.header_label8.text()
        dto.customer_company = self.header_label2.text()
        dto.customer_name = self.header_label2.text()
        dto.customer_phone = self.header_label2.text()
        dto.product_list = self.get_product_list()
        dto.create_user = self.tail_row3_label2.text()
        dto.order_manager = self.tail_row3_label4.text()
        dto.goods_sender = self.tail_row3_label6.text()
        dto.goods_receiver = self.tail_row3_label8.text()
        self.signal_ok.emit(self, dto)
        self.close()

    def get_product_list(self):
        count = self.table.rowCount()
        result = []
        for i in range(count):
            dto = OrderSaleProductDto()
            item1 = self.table.item(i, 1)
            if item1.tree_item is not None:
                tree_data = item1.tree_item.tree_data
                dto.product_info_id = tree_data[0]
                dto.product_type_id = tree_data[1]
            dto.unit_desc = self.table.cellWidget(i, 2).text()
            dto.count = self.table.cellWidget(i, 3).text()
            dto.price = self.table.cellWidget(i, 4).text()
            dto.desc = self.table.cellWidget(i, 5).text()
            result.append(dto)
        return result

    def onclick_cancel(self):
        self.close()

    def re_load_data(self):
        pass

    def add_row(self):
        index = self.table.rowCount()
        self.table.insertRow(index)
        index_item = QTableWidgetItem(str(index + 1))
        index_item.setFlags(Qt.ItemIsEnabled)
        index_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(index, 0, index_item)

        product_combobox = TreeComboBox()
        product_name_item = QTableWidgetItem()
        product_name_item.tree_item = None
        product_combobox.init_ui(product_name_item)
        product_combobox.signal_button_clicked.connect(self.on_product_combobox_clicked)
        product_combobox.signal_item_selected.connect(self.on_product_combobox_changed)
        self.table.setItem(index, 1, product_name_item)
        self.table.setCellWidget(index, 1, product_combobox)

        cell_item_unit = QTableWidgetItem()
        self.table.setItem(index, 2, cell_item_unit)
        item_unit = CellLineEdit(cell_item_unit, 2)
        item_unit.signal_clicked.connect(self.on_cell_edit_clicked)
        item_unit.signal_text_changed.connect(self.on_cell_edit_text_changed)
        item_unit.setAlignment(Qt.AlignCenter)
        item_unit.setObjectName("cell-number-edit")
        self.table.setCellWidget(index, 2, item_unit)

        cell_item_count = QTableWidgetItem()
        self.table.setItem(index, 3, cell_item_count)
        item_count = CellLineEdit(cell_item_count, 3)
        item_count.setValidator(self.reg_exp_validator)
        item_count.signal_clicked.connect(self.on_cell_edit_clicked)
        item_count.signal_text_changed.connect(self.on_cell_edit_text_changed)
        item_count.setObjectName("cell-number-edit")
        item_count.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(index, 3, item_count)

        cell_item_price = QTableWidgetItem()
        self.table.setItem(index, 4, cell_item_price)
        item_price = CellLineEdit(cell_item_price, 4)
        item_price.setValidator(self.reg_exp_validator)
        item_price.signal_clicked.connect(self.on_cell_edit_clicked)
        item_price.signal_text_changed.connect(self.on_cell_edit_text_changed)
        item_price.setObjectName("cell-number-edit")
        item_price.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(index, 4, item_price)

        cell_item_amount = QTableWidgetItem()
        self.table.setItem(index, 5, cell_item_amount)
        item_amount = CellLineEdit(cell_item_amount, 5)
        item_amount.setValidator(self.reg_exp_validator)
        item_amount.setEnabled(False)
        item_amount.signal_clicked.connect(self.on_cell_edit_clicked)
        item_amount.signal_text_changed.connect(self.on_cell_edit_text_changed)
        item_amount.setObjectName("cell-number-edit")
        item_amount.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(index, 5, item_amount)

        cell_item_desc = QTableWidgetItem()
        self.table.setItem(index, 6, cell_item_desc)
        item_desc = CellLineEdit(cell_item_desc, 6)
        item_desc.signal_clicked.connect(self.on_cell_edit_clicked)
        item_desc.signal_text_changed.connect(self.on_cell_edit_text_changed)
        item_desc.setObjectName("cell-number-edit")
        item_desc.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(index, 6, item_desc)

        bar = self.table.verticalScrollBar()
        if bar.maximum() == 0:
            self.scrollbar.setRange(bar.minimum(), bar.maximum())
        else:
            self.scrollbar.setRange(bar.minimum(), bar.maximum() + 1)
        self.scrollbar.setSingleStep(bar.singleStep())
        self.scrollbar.setPageStep(bar.pageStep())

    def remove_row(self):
        if self.select_row is not None:
            self.table.removeRow(self.select_row.row())
            self.select_row = None
            self.refresh_index()
            bar = self.table.verticalScrollBar()
            self.scrollbar.setRange(bar.minimum(), bar.maximum())
            self.scrollbar.setSingleStep(bar.singleStep())
            self.scrollbar.setPageStep(bar.pageStep())

    def init_data(self):
        """初始化数据"""
        order_info = OrderInfo()
        order_info = order_info.query_order_info_by_id(self.order_id)[0]
        self.order_name = order_info[1]
        self.order_type = order_info[2]
        self.company_name = order_info[3]
        self.company_address = order_info[4]
        self.tel_no = order_info[5]
        self.phone_no = order_info[6]
        self.qq_no = order_info[7]
        self.order_desc = order_info[8]
        # 标题
        self.header.setText(self.company_name + self.order_name + self.order_type)
        # 地址
        self.tail_row1_label2.setText(self.company_address)
        # 电话
        self.tail_row1_label4.setText(self.tel_no)
        # 手机
        self.tail_row1_label5.setText(self.phone_no)
        # QQ
        self.tail_row1_label7.setText(self.qq_no)
        # 备注
        self.tail_row2_label2.setText(self.order_desc)
        if self.new_add:
            self.setWindowTitle("新建" + self.order_type)
            self.init_order_no()
            self.tail_row3_label2.setText(self.current_user.full_name)
            self.tail_row3_label2.setEnabled(False)
            self.tail_row3_label4.setText(self.current_user.full_name)
            self.tail_row3_label4.setEnabled(False)

    def load_data(self, detail_id, detail_no):
        """加载数据库数据"""
        self.detail_id = detail_id
        pass

    def refresh_index(self):
        count = self.table.rowCount()
        for i in range(count):
            self.table.item(i, 0).setText(str(i + 1))

    def init_order_no(self):
        sale_list = OrderSaleList()
        upper = get_chinese_all_upper(self.order_type)
        prefix = upper[0:2]
        now = datetime.now().strftime("%Y-%m-%d")
        count = sale_list.fetch_count_by_order_id_date(self.order_id, now)
        index = str(count + 1)
        suffix = '-'
        for i in range(5 - len(index)):
            suffix += '0'
        suffix += index
        order_no = prefix + '-' + now + suffix
        self.header_label8.setText(order_no)

    def on_cell_edit_clicked(self, cell):
        if self.select_row:
            self.do_unselect_row(self.select_row)
        new_cell = self.table.item(cell.row(), 0)
        self.do_select_row(new_cell)
        self.select_row = new_cell

    def on_cell_edit_text_changed(self, cell, column, text):
        if column == 3:
            # 数量修改
            self.calc_amount()
        elif column == 4:
            # 单价修改
            self.calc_amount()

    def on_scrollbar_value_change(self, *args, **kwargs):
        item = self.table.item(args[0], 0)
        self.table.scrollToItem(item, QAbstractItemView.PositionAtTop)

    def on_product_combobox_clicked(self, cell_item: QTableWidgetItem):
        if self.select_row:
            self.do_unselect_row(self.select_row)
        new_cell = self.table.item(cell_item.row(), 0)
        self.do_select_row(new_cell)
        self.select_row = new_cell

    def on_product_combobox_changed(self, cell: QTableWidgetItem, item: QTreeWidgetItem):
        self.table.item(cell.row(), 1).tree_item = item
        self.table.cellWidget(cell.row(), 4).setText(item.tree_data[4])

    def on_cell_clicked(self, *args, **kwargs):
        cell = args[0]
        if self.select_row:
            self.do_unselect_row(self.select_row)
        new_cell = self.table.item(cell.row(), 0)
        self.do_select_row(new_cell)
        self.select_row = new_cell

    def do_select_row(self, cell):
        cell.setIcon(QIcon(':/icon/icons/select.png'))

    def do_unselect_row(self, cell):
        cell.setIcon(QIcon())

    def to_float(self, text):
        if text == '':
            return 0
        return float(text)

    def calc_amount(self):
        count = self.table.rowCount()
        product_count = 0
        product_amount = 0
        for row_index in range(count):
            item_count = self.to_float(self.table.cellWidget(row_index, 3).text())
            item_price = self.to_float(self.table.cellWidget(row_index, 4).text())
            item_amount = self.table.cellWidget(row_index, 5)
            row_amount = (item_count * item_price)
            item_amount.setText(str(row_amount))
            product_count += item_count
            product_amount += row_amount
        self.total_cell_count.setText(str(product_count))
        self.total_cell_num.setText(str(product_amount) + ' 元')
        money_format = num2money_format(str(product_amount))
        self.total_cell_cn.setText(money_format)
