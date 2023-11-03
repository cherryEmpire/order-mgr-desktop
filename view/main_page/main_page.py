from PySide6.QtWidgets import QWidget, QVBoxLayout

from view.main_page.navigation_bar import NavigationBar


class MainPage(QWidget):

    def init_ui(self, data):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_bar = NavigationBar()
        self.main_bar.init_ui(data)
        self.main_layout.addWidget(self.main_bar)
