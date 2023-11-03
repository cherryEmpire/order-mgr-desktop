from PySide6.QtWidgets import QWidget, QVBoxLayout


class DashBoard(QWidget):

    def init_ui(self, data):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
