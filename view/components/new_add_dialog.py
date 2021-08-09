# @Time   : 2021/8/7 4:03
# @Author   : 翁鑫豪
# @Description   : new_add_dialog.py
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialog, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton


class NewAddDialog(QDialog):
    signal_ok = Signal(object, object)

    def init_ui(self, title, keys):
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(':/icon/icons/main.png'))
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout(self)
        self.keys = keys
        self.edit_list = []

        for key in keys:
            edit = QLineEdit()
            self.form_layout.addRow(key, edit)
            self.edit_list.append(edit)

        self.main_layout.addLayout(self.form_layout)

        self.button_layout = QHBoxLayout(self)
        self.button_ok = QPushButton('确定')
        self.button_ok.setObjectName('operation-button')
        self.button_ok.clicked.connect(self.onclick_ok)
        self.button_cancel = QPushButton('取消')
        self.button_cancel.setObjectName('operation-button')
        self.button_cancel.clicked.connect(self.onclick_cancel)
        self.button_layout.addWidget(self.button_ok)
        self.button_layout.addWidget(self.button_cancel)

        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    def load_data(self, data, mode):
        if mode == 1:
            for i in range(len(data)):
                self.edit_list[i].setText(str(data[i]))
                self.edit_list[i].setEnabled(False)
        else:
            for i in range(len(data)):
                self.edit_list[i].setText(str(data[i]))

    def onclick_ok(self):
        data = []
        for edit in self.edit_list:
            data.append(edit.text())
        self.signal_ok.emit(self.keys, data)
        self.close()

    def onclick_cancel(self):
        self.close()
