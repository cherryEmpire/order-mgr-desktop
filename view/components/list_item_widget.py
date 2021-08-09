# @Time   : 2021/8/10 0:25
# @Author   : 翁鑫豪
# @Description   : list_item_widget.py
import typing

import PySide2
from PySide2 import QtGui
from PySide2.QtCore import Qt, Signal, QSize
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy

from utils.constants import SYSTEM_FONT


class ListItemWidget(QWidget):
    signal_edit_clicked = Signal(object)
    signal_view_clicked = Signal(object)

    def __init__(self, parent: typing.Optional[PySide2.QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setMargin(0)
        self.main_layout.setSpacing(0)
        self.label = QLabel(self)
        self.label.setFont(QFont(SYSTEM_FONT, 12))

        self.btn_widget = QWidget(self.label)
        self.btn_widget.setMaximumWidth(60)
        self.btn_widget_layout = QHBoxLayout(self.btn_widget)
        self.btn_widget_layout.setSpacing(0)
        self.btn_widget_layout.setMargin(0)

        self.view_button = QPushButton(self.btn_widget)
        self.view_button.setIcon(QIcon(':/icon/icons/view.png'))
        self.view_button.setObjectName('list-item-edit-button')

        self.edit_button = QPushButton(self.btn_widget)
        self.edit_button.setIcon(QIcon(':/icon/icons/edit.png'))
        self.edit_button.setObjectName('list-item-edit-button')

        self.main_layout.addWidget(self.label, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        self.btn_widget_layout.addWidget(self.view_button, alignment=Qt.AlignCenter)
        self.btn_widget_layout.addWidget(self.edit_button, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.btn_widget, alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.view_button.clicked.connect(self.on_view_click)
        self.edit_button.clicked.connect(self.on_edit_click)
        self.setLayout(self.main_layout)

    def on_edit_click(self):
        self.signal_edit_clicked.emit(self)

    def on_view_click(self):
        self.signal_view_clicked.emit(self)
