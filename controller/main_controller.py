# @Time   : 2021/8/7 0:04
# @Author   : 翁鑫豪
# @Description   : main_controller.py

from PySide2.QtCore import QObject

from db.user_info import UserInfo, UserDto
from view.components.common_components import MessageBox
from view.mainwindow.mainwindow import OrderMainWindow
from view.mainwindow.register import RegisterForm


class MainController(QObject):

    def __init__(self, login_form) -> None:
        super().__init__()
        self.login_form = login_form
        self.mainwindow: OrderMainWindow = None
        self.current_user:UserDto = None

    def do_click_login(self, name, password):
        user_info = UserInfo()
        result = user_info.query_user_by_name(name)
        if result is None or len(result) == 0:
            self.error_box = MessageBox(text='用户名' + name + '不存在！')
            self.error_box.setWindowTitle("错误")
            self.error_box.show()
            return
        user = result[0]
        if user[0] == name and user[2] == password:
            self.current_user = UserDto(user[0], user[1], None)
            self.show_mainwindow()
        else:
            self.error_box = MessageBox(text='用户名或密码错误！')
            self.error_box.setWindowTitle("错误")
            self.error_box.show()
            return

    def do_click_register(self, obj):
        self.login_form.hide()
        self.register_form = RegisterForm()
        self.register_form.login_form = self.login_form
        self.register_form.signal_register_new.connect(self.do_register_user)
        self.register_form.show()

    def do_register_user(self, data):
        user_info = UserInfo()
        user_info.insert_user_info(data[0], data[1], data[2])


    def show_mainwindow(self):
        self.login_form.close()
        self.mainwindow = OrderMainWindow()
        self.mainwindow.init_ui(self.current_user)
        self.mainwindow.show()
