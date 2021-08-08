# @Time   : 2021/8/8 4:16
# @Author   : 翁鑫豪
# @Description   : tree_combobox.py

import PySide2
from PySide2 import QtWidgets
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QHBoxLayout, QTreeView, QFrame, QTreeWidget, QTreeWidgetItem, QWidget, QToolButton, QMenu, QWidgetAction, QSizePolicy

from db.product_info import ProductInfo
from db.product_type import ProductType


class CustomQToolButton(QToolButton):

    def defaultAction(self) -> PySide2.QtWidgets.QAction:
        return super().defaultAction()

    def showMenu(self) -> None:
        super().showMenu()


class CustomMenu(QMenu):
    signal_clicked = Signal(object)

    def show(self) -> None:
        super().show()

    def showEvent(self, event: PySide2.QtGui.QShowEvent) -> None:
        self.signal_clicked.emit(self)
        super().showEvent(event)


class TreeComboBox(QWidget):
    signal_button_clicked = Signal(object)
    signal_item_selected = Signal(object, object)

    def init_ui(self, cell_item):
        self.cell_item = cell_item
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setMargin(0)
        self.main_layout.setSpacing(5)
        self.tool_btn = CustomQToolButton(self)
        self.tool_btn.setObjectName('TreeComboBox-QToolButton')
        self.tool_btn.setStyleSheet("QToolButton::menu-indicator{width:15px; height:15px; margin: 5px;}")
        self.tool_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tool_btn.setPopupMode(QToolButton.InstantPopup)
        self.menu = CustomMenu(self)
        self.menu.signal_clicked.connect(self.on_tool_btn_click)

        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.header().setVisible(False)
        self.tree.setFrameShape(QFrame.NoFrame)
        self.tree.setEditTriggers(QTreeView.NoEditTriggers)

        self.action = QWidgetAction(self.tree)
        self.action.setDefaultWidget(self.tree)
        self.menu.addAction(self.action)
        self.tool_btn.setMenu(self.menu)
        self.main_layout.addWidget(self.tool_btn)
        self.tree.itemClicked.connect(self.on_tree_item_clicked)

        self.load_data()

    def resizeEvent(self, event: PySide2.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.tree.setMinimumWidth(self.width() - 5)

    def load_data(self):
        product_type = ProductType()
        product_info = ProductInfo()
        data = product_type.fetch_data()
        for type_item in data:
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, type_item[1])
            parent.tree_data = type_item
            parent.leaf = False
            self.tree.addTopLevelItem(parent)
            product_infos = product_info.fetch_data_by_product_type(type_item[0])
            for product_info_item in product_infos:
                child = QTreeWidgetItem()
                child.tree_data = product_info_item
                child.leaf = True
                child.setText(0, product_info_item[2])
                child.setText(1, product_info_item[4])
                parent.addChild(child)

    def on_tree_item_clicked(self, *args, **kwargs):
        item: QTreeWidgetItem = args[0]
        if item.leaf:
            self.tool_btn.setText(item.tree_data[2])
            self.menu.hide()
            self.signal_item_selected.emit(self.cell_item, item)

    def on_tool_btn_click(self, item):
        self.signal_button_clicked.emit(self.cell_item)
