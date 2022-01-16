from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QMainWindow,  QWidget, QGridLayout, QLineEdit, QPushButton, QListWidget, QInputDialog)

from pyside2_demo.internal.views.common import set_widget_on_screen_center, QHLine


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        # 初始化圖形控件
        in_line = QLineEdit()
        add_btn = QPushButton("新增")
        add_btn.clicked.connect(self.add_btn_fn)
        h_line = QHLine()
        list_widget = QListWidget()
        rename_btn = QPushButton("重新命名")
        rename_btn.clicked.connect(self.rename_btn_fn)
        del_btn = QPushButton("刪除")
        del_btn.clicked.connect(self.del_btn_fn)
        del_all_btn = QPushButton("刪除全部")
        del_all_btn.clicked.connect(self.del_all_btn_fn)

        # 設定 layout
        layout = QGridLayout()
        layout.addWidget(in_line, 0, 0)
        layout.addWidget(add_btn, 0, 1)
        layout.addWidget(h_line, 1, 0, 1, 2)
        layout.addWidget(list_widget, 2, 0, 3, 1)
        layout.addWidget(rename_btn, 2, 1)
        layout.addWidget(del_btn, 3, 1)
        layout.addWidget(del_all_btn, 4, 1)

        # 設定 widget 參數
        self.in_line = in_line
        self.list_widget = list_widget
        self.setLayout(layout)

    @Slot()
    def add_btn_fn(self):
        text = self.in_line.text()
        self.list_widget.addItem(text)

    @Slot()
    def rename_btn_fn(self):
        curr_item = self.list_widget.currentItem()
        idx = self.list_widget.row(curr_item)
        text = curr_item.text()
        replace_text, _ = QInputDialog.getText(
            self, "Item", "Enter new item", QLineEdit.Normal, text)
        if replace_text:
            self.list_widget.takeItem(idx)  # 移除選擇的item
            self.list_widget.insertItem(idx, replace_text)
            self.list_widget.setCurrentRow(idx)

    @Slot()
    def del_btn_fn(self):
        idx = self.list_widget.currentRow()
        if idx != -1:
            self.list_widget.takeItem(idx)  # 移除選擇的item

    @Slot()
    def del_all_btn_fn(self):
        if self.list_widget.count() != -1:
            self.list_widget.clear()  # 移除全部的item


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        set_widget_on_screen_center(self, 400, 300)
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Example03")
