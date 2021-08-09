import sys
from pathlib import Path

from PySide2.QtCore import QFile, QElapsedTimer, QByteArray
from PySide2.QtWidgets import QApplication

from controller.main_controller import MainController
from db.init_db import system_init_db_step
from db.user_info import UserDto
from utils.system_util import get_home_abs_path
from view.mainwindow.login import LoginForm
from view.mainwindow.mainwindow import OrderMainWindow
from view.mainwindow.splash_screen import SystemSplashScreen
from static import ordermgr


class SystemStartCheck:

    def __init__(self) -> None:
        super().__init__()
        self.__check_home_path()
        self.__init_db()

    def __check_home_path(self):
        home_path = get_home_abs_path()
        if home_path.exists():
            return
        Path.mkdir(home_path)

    def __init_db(self):
        system_init_db_step()


class MainApp:

    def __init__(self) -> None:
        SystemStartCheck()
        self.app = QApplication(sys.argv)
        self.load_qss()

        # self.splash = SystemSplashScreen()
        # self.splash.init_ui()
        # self.splash.show()
        # self.app.processEvents()
        # self.login_form = LoginForm()
        #
        # timer = QElapsedTimer()
        # timer.start()
        # splash_time = 1000
        # max_percent = splash_time / 100
        # while timer.elapsed() < splash_time:
        #     QApplication.processEvents()
        #     timer.elapsed() / max_percent
        #     self.splash.progress_bar.setValue(timer.elapsed() / max_percent)
        # self.splash.finish(self.login_form)
        # self.splash.deleteLater()
        # self.main_controller = MainController(self.login_form)
        # self.login_form.signal_login.connect(self.main_controller.do_click_login)
        # self.login_form.signal_register.connect(self.main_controller.do_click_register)
        # self.login_form.show()
        self.test()
        self.app.exec_()

    def load_qss(self):
        q_file = QFile(":/qss/qss/sale.qss")
        if q_file.open(QFile.ReadOnly):
            strStyleSheet: QByteArray = q_file.readAll()
            str1 = str(strStyleSheet, encoding='utf-8')
            q_file.close()
            self.app.setStyleSheet(str1)

    def test(self):
        self.mainwindow = OrderMainWindow()
        user = UserDto('admin', '测试', None)
        self.mainwindow.init_ui(user)
        self.mainwindow.show()


if __name__ == '__main__':
    MainApp()
