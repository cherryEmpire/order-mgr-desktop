# @Time   : 2021/8/6 21:46
# @Author   : 翁鑫豪
# @Description   : splash_screen.py
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QPixmap
from PySide2.QtWidgets import QProgressBar, QSplashScreen, QVBoxLayout, QLabel

from utils.constants import SYSTEM_FONT


class SplashQProgressBar(QProgressBar):
    def init_ui(self):
        pass


class SystemSplashScreen(QSplashScreen):

    def init_ui(self):
        self.setPixmap(QPixmap(":/image/images/splash.jpg"))
        self.setFont(QFont(SYSTEM_FONT, 10))

        layout = QVBoxLayout()

        q_label = QLabel()
        q_label.setText("销售单管理系统")
        q_label.setObjectName('logo_name')
        q_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(q_label)

        q_label1 = QLabel()
        q_label1.setText("copyright@一叶飘零")
        q_label1.setObjectName('logo_copyright')
        q_label1.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        layout.addWidget(q_label1)

        q_progress_bar = SplashQProgressBar()
        q_progress_bar.setObjectName('init_progress')
        q_progress_bar.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        layout.addWidget(q_progress_bar)

        layout.setStretchFactor(q_label, 17)
        layout.setStretchFactor(q_label1, 2)
        layout.setStretchFactor(q_progress_bar, 1)
        self.progress_bar = q_progress_bar
        self.setLayout(layout)
