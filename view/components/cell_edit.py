# @Time   : 2021/8/8 15:33
# @Author   : 翁鑫豪
# @Description   : cell_edit.py

import PySide6
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QLineEdit


class CellLineEdit(QLineEdit):
    signal_clicked = Signal(object)
    signal_text_changed = Signal(object, object, object)

    def __init__(self, cell, column) -> None:
        super().__init__()
        self.textChanged.connect(self.do_text_changed)
        self.cell = cell
        self.column = column

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.signal_clicked.emit(self.cell)
        super().mousePressEvent(event)

    def do_text_changed(self, text):
        self.signal_text_changed.emit(self.cell, self.column, text)
