# @Time   : 2021/8/7 0:02
# @Author   : 翁鑫豪
# @Description   : register.py
import PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from db.user_info import UserInfo
from view.components.common_components import PasswordEdit, MessageBox


class RegisterForm(QtWidgets.QWidget):
    """Basic login form."""
    signal_register_new = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
        self.main_controller = None
        self.last_mouse_position = None
        self.login_form = None

    def setup_ui(self):
        """Setup the login form.
        """
        self.resize(480, 520)
        self.setWindowFlags(Qt.Dialog | QtCore.Qt.FramelessWindowHint)

        self.setStyleSheet(
            """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #cf7500;
                border-style: inset;
            }
            QPushButton:pressed {
                background-color: #ffa126;
                border-style: inset;
            }
            """
        )

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.sub_layout = QtWidgets.QHBoxLayout()

        self.widget = QtWidgets.QWidget(self)
        self.widget.setStyleSheet(".QWidget{background-color: rgb(20, 20, 40);}")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(9, 0, 0, 0)

        self.sub_layout1 = QtWidgets.QVBoxLayout()
        self.sub_layout1.setContentsMargins(-1, 15, -1, -1)

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(80, 80))
        self.label.setMaximumSize(QtCore.QSize(80, 80))
        self.label.setStyleSheet("image: url(:/icon/icons/rocket_48x48.png);")
        self.sub_layout1.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setContentsMargins(50, 35, 59, -1)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("color: rgb(231, 231, 231);\n"
                                   "font: 15pt \"Verdana\";")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.username_edit = QtWidgets.QLineEdit(self.widget)
        self.username_edit.setMinimumSize(QtCore.QSize(0, 40))
        self.username_edit.setStyleSheet("QLineEdit {\n"
                                         "color: rgb(231, 231, 231);\n"
                                         "font: 15pt \"Verdana\";\n"
                                         "border: None;\n"
                                         "border-bottom-color: white;\n"
                                         "border-radius: 10px;\n"
                                         "padding: 0 8px;\n"
                                         "background: rgb(20, 20, 40);\n"
                                         "selection-background-color: darkgray;\n"
                                         "}")
        self.username_edit.setFocus()
        self.username_edit.setPlaceholderText("用户名")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.username_edit)

        self.label_fullname = QtWidgets.QLabel(self.widget)
        self.label_fullname.setStyleSheet("color: rgb(231, 231, 231);\n"
                                          "font: 15pt \"Verdana\";")
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_fullname)

        self.label_4 = QtWidgets.QLabel(self.widget)
        self.form_layout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_4)

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.form_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.fullname_edit = QtWidgets.QLineEdit(self.widget)
        self.fullname_edit.setMinimumSize(QtCore.QSize(0, 40))
        self.fullname_edit.setStyleSheet("QLineEdit {\n"
                                         "color: rgb(231, 231, 231);\n"
                                         "font: 15pt \"Verdana\";\n"
                                         "border: None;\n"
                                         "border-bottom-color: white;\n"
                                         "border-radius: 10px;\n"
                                         "padding: 0 8px;\n"
                                         "background: rgb(20, 20, 40);\n"
                                         "selection-background-color: darkgray;\n"
                                         "}")
        self.fullname_edit.setPlaceholderText("姓名")
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.fullname_edit)

        self.password_edit = PasswordEdit(self.widget)
        self.password_edit.setPlaceholderText("密码")
        self.password_edit.setMinimumSize(QtCore.QSize(0, 40))
        self.password_edit.setStyleSheet("QLineEdit {\n"
                                         "color: rgb(231, 231, 231);\n"
                                         "font: 15pt \"Verdana\";\n"
                                         "border: None;\n"
                                         "border-bottom-color: white;\n"
                                         "border-radius: 10px;\n"
                                         "padding: 0 8px;\n"
                                         "background: rgb(20, 20, 40);\n"
                                         "selection-background-color: darkgray;\n"
                                         "}")
        self.form_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.password_edit)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.password_confirm = PasswordEdit(self.widget)
        self.password_confirm.setPlaceholderText("确认密码")
        self.password_confirm.setMinimumSize(QtCore.QSize(0, 40))
        self.password_confirm.setStyleSheet("QLineEdit {\n"
                                            "color: rgb(231, 231, 231);\n"
                                            "font: 15pt \"Verdana\";\n"
                                            "border: None;\n"
                                            "border-bottom-color: white;\n"
                                            "border-radius: 10px;\n"
                                            "padding: 0 8px;\n"
                                            "background: rgb(20, 20, 40);\n"
                                            "selection-background-color: darkgray;\n"
                                            "}")
        self.form_layout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.password_confirm)
        self.password_confirm.setEchoMode(QtWidgets.QLineEdit.Password)

        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("border: 2px solid white;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.line)

        self.line_3 = QtWidgets.QFrame(self.widget)
        self.line_3.setStyleSheet("border: 2px solid white;")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.form_layout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.line_3)

        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setStyleSheet("border: 2px solid white;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.form_layout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.line_2)

        self.line_4 = QtWidgets.QFrame(self.widget)
        self.line_4.setStyleSheet("border: 2px solid white;")
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.form_layout.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.line_4)

        self.register_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.register_button.sizePolicy().hasHeightForWidth())

        self.register_button.setSizePolicy(sizePolicy)
        self.register_button.setMinimumSize(QtCore.QSize(0, 60))
        self.register_button.setAutoFillBackground(False)
        self.register_button.setStyleSheet("color: rgb(231, 231, 231);\n"
                                           "font: 17pt \"Verdana\";\n"
                                           "border: 2px solid orange;\n"
                                           "padding: 5px;\n"
                                           "border-radius: 3px;\n"
                                           "opacity: 200;\n"
                                           "")
        self.register_button.setAutoDefault(True)
        self.form_layout.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.register_button)

        self.cancel_button = QtWidgets.QPushButton(self.widget)
        self.cancel_button.setMinimumSize(QtCore.QSize(0, 60))
        self.cancel_button.setStyleSheet("color: rgb(231, 231, 231);\n"
                                         "font: 17pt \"Verdana\";\n"
                                         "border: 2px solid orange;\n"
                                         "padding: 5px;\n"
                                         "border-radius: 3px;\n"
                                         "opacity: 200;\n"
                                         "")
        self.cancel_button.setDefault(False)
        self.cancel_button.setFlat(False)
        self.form_layout.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.cancel_button)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.form_layout.setItem(8, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.sub_layout1.addLayout(self.form_layout)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.sub_layout1.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.sub_layout1)

        self.sub_layout.addWidget(self.widget)
        self.sub_layout.setStretch(0, 1)
        self.main_layout.addLayout(self.sub_layout)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "登录"))
        # self.close_button.setText(_translate("Form", "X"))
        self.label_2.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icon/icons/user_32x32.png\"/></p></body></html>"))
        self.label_fullname.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icon/icons/user_32x32.png\"/></p></body></html>"))
        self.label_3.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icon/icons/lock_32x32.png\"/></p></body></html>"))
        self.label_4.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icon/icons/lock_32x32.png\"/></p></body></html>"))
        self.register_button.setText(_translate("Form", "注册"))
        self.cancel_button.setText(_translate("Form", "取消"))
        self.register_button.clicked.connect(self.do_click_register)
        self.cancel_button.clicked.connect(self.do_click_cancel)

    def do_click_register(self):
        name = self.username_edit.text()
        password = self.password_edit.text()
        fullname = self.fullname_edit.text()
        password_confirm = self.password_confirm.text()
        if name == '' or password == '' or password_confirm == '':
            self.error_box = MessageBox(text='用户名或密码为空！')
            self.error_box.setWindowTitle("错误")
            self.error_box.show()
            return
        if password != password_confirm:
            self.error_box = MessageBox(text='两次输入的密码不一致！')
            self.error_box.setWindowTitle("错误")
            self.error_box.show()
            return
        user_info = UserInfo()
        if user_info.user_exist(name):
            self.error_box = MessageBox(text='用户名已存在！')
            self.error_box.setWindowTitle("错误")
            self.error_box.show()
            return
        data = [name, fullname, password]
        self.signal_register_new.emit(data)
        self.close()
        self.login_form.username_edit.setText(name)
        self.login_form.show()

    def do_click_cancel(self):
        self.close()
        self.login_form.show()

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if event.buttons() != Qt.LeftButton:
            return
        if self.last_mouse_position is None:
            self.last_mouse_position = event.globalPos()
            return
        position = self.pos() + event.globalPos() - self.last_mouse_position
        self.move(position.x(), position.y())
        self.last_mouse_position = event.globalPos()

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.last_mouse_position = event.globalPos()
