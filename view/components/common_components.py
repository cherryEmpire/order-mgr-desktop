# @Time   : 2021/8/6 23:27
# @Author   : 翁鑫豪
# @Description   : common_components.py
from typing import Union

from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QLineEdit, QMessageBox, QItemDelegate


class PasswordEdit(QLineEdit):
    """
    A LineEdit with icons to show/hide password entries
    """
    CSS = """QLineEdit {
        border-radius: 0px;
        height: 30px;
        margin: 0px 0px 0px 0px;
    }
    """

    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)

        # Set styles
        # self.setStyleSheet(self.CSS)

        self.visibleIcon = QIcon(":/icon/icons/eye_on.png")
        self.hiddenIcon = QIcon(":/icon/icons/eye_off.png")

        self.setEchoMode(QLineEdit.Password)
        self.togglepasswordAction = self.addAction(self.visibleIcon, QLineEdit.TrailingPosition)
        self.togglepasswordAction.triggered.connect(self.on_toggle_password_Action)
        self.password_shown = False

    def on_toggle_password_Action(self):
        if not self.password_shown:
            self.setEchoMode(QLineEdit.Normal)
            self.password_shown = True
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.setEchoMode(QLineEdit.Password)
            self.password_shown = False
            self.togglepasswordAction.setIcon(self.visibleIcon)


class MessageBox(QMessageBox):

    def __init__(self, *args, **kwargs):
        super(MessageBox, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon(':/icon/icons/main.png'))
        self.setStandardButtons(self.Close)  # 关闭按钮
        self.closeBtn = self.button(self.Close)  # 获取关闭按钮
        self.closeBtn.setText('关闭')


class ReadOnlyDelegate(QItemDelegate):

    def createEditor(self, parent: QtWidgets.QWidget, option: QtWidgets.QStyleOptionViewItem, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> QtWidgets.QWidget:
        return None