from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy

sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class NavigationItem(QWidget):

    def init_ui(self, data=None):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        self.item_button = QPushButton(data)
        self.item_button.setSizePolicy(sizePolicy)
        self.main_layout.addWidget(self.item_button)


class NavigationType(QWidget):
    def init_ui(self, data=None):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.type_button = QPushButton(data['type'])
        self.type_button.setSizePolicy(sizePolicy)
        self.main_layout.addWidget(self.type_button)
        subtypes = data['subtype']
        self.children = []
        for sub in subtypes:
            item = NavigationItem()
            item.init_ui(sub)
            self.children.append(item)
            self.main_layout.addWidget(item)


class NavigationBar(QWidget):
    def init_ui(self, data=None):
        self.setMaximumWidth(200)
        if data is None:
            data = []
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        self.types = []

        for item in data:
            t1 = NavigationType()
            t1.init_ui(item)
            self.types.append(t1)
            self.main_layout.addWidget(t1)
