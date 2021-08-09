# @Time   : 2021/8/7 17:32
# @Author   : 翁鑫豪
# @Description   : order_info_form.py
from PySide2.QtCore import Signal, QRegExp
from PySide2.QtGui import Qt, QRegExpValidator, QStandardItemModel, QStandardItem, QIcon
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QFormLayout, QTextEdit, QComboBox


class OrderInfoForm(QDialog):
    signal_ok = Signal(object, object)

    def init_ui(self):
        self.tel_reg_exp = QRegExp("^(-?\d+)(\-\d+)?$")
        self.tel_reg_exp_validator = QRegExpValidator(self.tel_reg_exp, self)

        self.phone_reg_exp = QRegExp("^(-?\d+)(\d+)?$")
        self.phone_reg_exp_validator = QRegExpValidator(self.phone_reg_exp, self)

        self.setWindowIcon(QIcon(':/icon/icons/main.png'))
        self.setWindowTitle("新增销售单据")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout(self)

        self.init_input_items()

        self.main_layout.addLayout(self.form_layout)

        self.button_layout = QHBoxLayout(self)
        self.button_ok = QPushButton('确定')
        self.button_ok.clicked.connect(self.onclick_ok)
        self.button_cancel = QPushButton('取消')
        self.button_cancel.clicked.connect(self.onclick_cancel)
        self.button_layout.addWidget(self.button_ok)
        self.button_layout.addWidget(self.button_cancel)

        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    def onclick_ok(self):
        data = []
        data.append(self.order_name.text())
        data.append(self.order_type.currentText())
        data.append(self.company_name.text())
        data.append(self.company_address.text())
        data.append(self.tel_no.text())
        data.append(self.phone_no.text())
        data.append(self.qq_no.text())
        data.append(self.order_desc.toPlainText())
        self.signal_ok.emit(None, data)
        self.close()

    def onclick_cancel(self):
        self.close()

    def init_input_items(self):
        self.order_name = QLineEdit(self)
        self.form_layout.addRow("单据名称", self.order_name)

        self.order_type = QComboBox(self)
        self.form_layout.addRow("单据类型", self.order_type)

        self.company_name = QLineEdit(self)
        self.form_layout.addRow("公司名称", self.company_name)

        self.company_address = QLineEdit(self)
        self.form_layout.addRow("公司地址", self.company_address)

        self.tel_no = QLineEdit(self)
        self.tel_no.setValidator(self.tel_reg_exp_validator)
        self.form_layout.addRow("联系人电话", self.tel_no)

        self.phone_no = QLineEdit(self)
        self.phone_no.setValidator(self.phone_reg_exp_validator)
        self.form_layout.addRow("联系人手机", self.phone_no)

        self.qq_no = QLineEdit(self)
        self.qq_no.setValidator(self.phone_reg_exp_validator)
        self.form_layout.addRow("联系人QQ", self.qq_no)

        self.order_desc = QTextEdit(self)
        self.form_layout.addRow("备注", self.order_desc)
        self.load_order_type()

    def load_order_type(self):
        desc = ['销售单', '采购单', '详情单']
        model = QStandardItemModel()
        for item_text in desc:
            item = QStandardItem()
            item.setText(item_text)
            model.appendRow(item)
        self.order_type.setModel(model)

    def load_data(self, data, mode):
        self.order_name.setText(data[0])
        self.order_type.setCurrentText(data[1])
        self.company_name.setText(data[2])
        self.company_address.setText(data[3])
        self.tel_no.setText(data[4])
        self.phone_no.setText(data[5])
        self.qq_no.setText(data[6])
        self.order_desc.setPlainText(data[7])
        if mode == 1:
            self.order_name.setEnabled(False)
            self.order_type.setEnabled(False)
            self.company_name.setEnabled(False)
            self.company_address.setEnabled(False)
            self.tel_no.setEnabled(False)
            self.phone_no.setEnabled(False)
            self.qq_no.setEnabled(False)
            self.order_desc.setEnabled(False)
