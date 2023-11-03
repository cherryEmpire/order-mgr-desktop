# @Time   : 2021/8/7 18:05
# @Author   : 翁鑫豪
# @Description   : item_combobox.py
from PySide6.QtCore import Signal
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QVBoxLayout, QWidget, QComboBox


class ItemComboBox(QWidget):
    signal_item_changed = Signal(object)

    def init_ui(self):
        self.model: QStandardItemModel = None
        self.current_index = None
        self.main_layout = QVBoxLayout(self)
        self.combobox = QComboBox(self)
        self.main_layout.addWidget(self.combobox)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.combobox.currentIndexChanged.connect(self.current_index_changed)

    def set_model(self, model: QStandardItemModel):
        self.model = model
        self.combobox.setModel(model)

    def current_index_changed(self, *args, **kwargs):
        self.current_index = args[0]

    def get_data(self):
        return self.model.item(self.current_index)
