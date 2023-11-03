import sys

from PySide6.QtWidgets import QApplication, QDialog, QHBoxLayout

from view.main_page.main_page import MainPage

if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = QDialog()
    form.setWindowTitle("测试")
    form.setMinimumWidth(800)
    form.setMinimumHeight(600)

    main = QHBoxLayout()
    page = MainPage()
    page.init_ui([
        {"type": "首页", "subtype": []},
        {"type": "收银", "subtype": []},
        {"type": "订单管理", "subtype": []},
        {"type": "商品管理", "subtype": ['商品大类', '商品明细']},
        {"type": "出入库", "subtype": ['入库', '出库']}
    ])
    main.addWidget(page)
    form.setLayout(main)
    form.show()
    app.exec()
