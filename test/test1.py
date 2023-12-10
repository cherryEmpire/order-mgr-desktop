import sys

from PySide6.QtGui import Qt, QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWidgets import QApplication, QWidget,QTreeWidget, QDialog, QMenu, QInputDialog, QMessageBox, QTreeWidgetItem, \
    QHBoxLayout, QHeaderView

from static import ordermgr

class MyApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        # 创建一个QTreeView控件，并设置其orientation属性为Qt.Vertical。
        self.tree_view = QTreeView()
        # self.tree_view.set
        # self.tree_view.setOrientation(Qt.Vertical)

        # 为QTreeView控件添加根节点。
        self.root_item = QTreeWidgetItem()

        # 为QTreeView控件添加右键菜单，用于新增、删除、修改商品类别。
        self.menu = QMenu(self.tree_view)
        self.menu.addAction("新增商品大类")
        self.menu.addAction("删除商品大类")
        self.menu.addAction("修改商品大类")
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.on_custom_context_menu_requested)

        # 显示窗口。
        self.tree_view.show()

    def on_custom_context_menu_requested(self, point):
        # 获取鼠标点击的节点。
        item = self.tree_view.itemAt(point)

        # 判断鼠标点击的节点是否为根节点。
        if item == self.root_item:
            # 根节点只能新增商品大类。
            self.menu.exec_(self.tree_view.mapToGlobal(point))
        else:
            # 非根节点可以新增、删除、修改商品类别。
            self.menu.exec_(self.tree_view.mapToGlobal(point))

    def on_action_add_clicked(self):
        # 新增商品大类。
        new_text, ok = QInputDialog.getText(self, "新增商品大类", "请输入名称：")
        if ok:
            new_item = QTreeWidgetItem(self.root_item)
            new_item.setText(0, new_text)
            new_item.setExpanded(False)

    def on_action_delete_clicked(self):
        # 删除商品大类。
        if item == self.root_item:
            return

        # 弹出对话框询问是否要删除。
        reply = QMessageBox.question(self, "删除商品大类", "确定要删除吗？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 删除节点及其子节点。
            item.parent().removeChild(item)

    def on_action_edit_clicked(self):
        # 修改商品大类。
        new_text, ok = QInputDialog.getText(self, "修改商品大类", "请输入新的名称：")
        if ok:
            item.setText(0, new_text)


class ProductTypeTree(QWidget):

    def init_ui(self):
        main = QHBoxLayout()
        self.tree_widget = QTreeWidget()
        self.tree_widget.headerItem().setText(0, "商品大类")
        self.tree_widget.headerItem().setText(1, "商品类别")

        self.tree_widget.setStyleSheet("""
                    QTreeWidget::item {
                font-size: 18px;
                font-weight: bold;
            }
                """)

        item = QTreeWidgetItem()
        item.setIcon(0, QIcon(':/icon/icons/main.png'))
        item.setText(0, "zzz")
        item1 = QTreeWidgetItem()
        item1.setText(1, "xiao")
        item1.setIcon(1, QIcon(':/icon/icons/main.png'))
        item.addChild(item1)
        self.tree_widget.addTopLevelItem(item)

        self.menu = QMenu(self.tree_widget)
        self.menu.addAction("新增商品大类")
        self.menu.addAction("删除商品大类")
        self.menu.addAction("修改商品大类")

        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.on_custom_context_menu_requested)

        main.addWidget(self.tree_widget)
        self.setLayout(main)

    def on_custom_context_menu_requested(self, point):
        zz = self.tree_widget.mapToGlobal(point)
        # 创建一个 QMenu 控件。
        menu = QMenu(self.tree_widget)

        # 将菜单项添加到 QMenu 控件中。
        menu.addAction("新增")


        item = self.tree_widget.itemAt(point)

        # 判断鼠标位置是否在树的节点上。
        if item is not None:
            # 鼠标位置在树的节点上。
            menu.addAction("删除")
            menu.addAction("修改")
            print("鼠标位置在节点 {} 上".format(item.text(0)))
        else:
            # 鼠标位置不在树的节点上。
            print("鼠标位置不在任何节点上")

        # 显示菜单。
        menu.exec(zz)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = QDialog()
    form.setWindowTitle("测试")
    form.setMinimumWidth(800)
    form.setMinimumHeight(600)

    main = QHBoxLayout()
    tree_widget = ProductTypeTree()
    tree_widget.init_ui()
    main.addWidget(tree_widget)
    form.setLayout(main)
    form.show()
    app.exec()
    sys.exit(app.exec())
