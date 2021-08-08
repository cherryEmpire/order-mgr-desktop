# @Time   : 2021/8/6 22:07
# @Author   : 翁鑫豪
# @Description   : mainwindow.py
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QMainWindow, QAction, QToolBar, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy

from controller.mainwindow_toolbar_controller import MainWindowToolBarContext
from db.user_info import UserDto
from utils.constants import SYSTEM_FONT
from view.order.order_list import OrderList
from view.order.order_list_item_table import OrderListItemTable
from view.product.product_info_table import ProductInfoTable
from view.product.product_type_list import ProductTypeList


class OrderMainWindow(QMainWindow):
    """主界面"""

    def init_ui(self, current_user):
        self.current_user: UserDto = current_user
        self.setWindowTitle("销售单管理系统")
        self.setWindowIcon(QIcon(':/icon/icons/main.png'))
        self.setMinimumWidth(1080)
        self.setMinimumHeight(720)
        self.init_toolbar()
        self.init_window()

    def init_toolbar(self):
        """初始化工具栏"""
        self.toolbar_context = MainWindowToolBarContext(self, self.current_user)
        tool_bar = QToolBar()

        self.tool_bar_open_order = QAction(QIcon(':/icon/icons/order.png'), '销售单据', self)
        self.tool_bar_open_order.triggered.connect(self.toolbar_context.open_order)
        tool_bar.addAction(self.tool_bar_open_order)

        self.tool_bar_open_product = QAction(QIcon(':/icon/icons/product.png'), '商品类库', self)
        self.tool_bar_open_product.triggered.connect(self.toolbar_context.open_product)
        tool_bar.addAction(self.tool_bar_open_product)

        self.tool_bar_open_help = QAction(QIcon(':/icon/icons/help.png'), '帮助', self)
        self.tool_bar_open_help.triggered.connect(self.toolbar_context.open_help)
        tool_bar.addAction(self.tool_bar_open_help)

        self.tool_bar_open_about = QAction(QIcon(':/icon/icons/about.png'), '关于', self)
        self.tool_bar_open_about.triggered.connect(self.toolbar_context.open_about)
        tool_bar.addAction(self.tool_bar_open_about)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tool_bar.addWidget(spacer)

        name_label = QLabel(self.current_user.full_name)
        name_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        q_font = QFont(SYSTEM_FONT, 16)
        q_font.setBold(True)
        name_label.setFont(q_font)

        tool_bar.addWidget(name_label)
        tool_bar.setMovable(False)
        tool_bar.setIconSize(QSize(32, 32))
        self.tool_bar = tool_bar

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, tool_bar)

    def init_window(self):
        self.main_frame = QWidget()
        self.left_frame = QWidget()
        self.right_frame = QWidget()

        self.main_layout = QHBoxLayout(self.main_frame)
        self.main_layout.setMargin(0)
        self.main_layout.setSpacing(0)

        self.left_layout = QVBoxLayout(self.left_frame)
        self.left_layout.setMargin(0)
        self.left_layout.setSpacing(0)

        self.right_layout = QVBoxLayout(self.right_frame)
        self.right_layout.setMargin(0)
        self.right_layout.setSpacing(0)

        self.init_order_list()
        self.init_order_info_table()

        self.init_product_type_list()
        self.init_product_info_table()

        self.main_layout.addWidget(self.left_frame, 1)
        self.main_layout.addWidget(self.right_frame, 3)
        self.setCentralWidget(self.main_frame)

    def init_order_list(self):
        self.order_list = OrderList(self.left_frame)
        self.order_list.init_ui()
        self.order_list.setVisible(True)
        self.order_list.signal_item_click.connect(self.toolbar_context.on_click_order_list_item)
        self.left_layout.addWidget(self.order_list, 1)

    def init_order_info_table(self):
        self.order_list_item_table = OrderListItemTable(self.right_frame)
        self.order_list_item_table.init_ui()
        self.order_list_item_table.setVisible(False)
        self.right_layout.addWidget(self.order_list_item_table, 1)

    def init_product_type_list(self):
        self.product_type_list = ProductTypeList(self.left_frame)
        self.product_type_list.init_ui()
        self.product_type_list.setVisible(False)
        self.product_type_list.signal_item_click.connect(self.toolbar_context.on_click_product_type_list_item)
        self.left_layout.addWidget(self.product_type_list, 1)

    def init_product_info_table(self):
        self.product_info_table = ProductInfoTable(self.right_frame)
        self.product_info_table.init_ui()
        self.product_info_table.setVisible(False)
        self.right_layout.addWidget(self.product_info_table, 1)
