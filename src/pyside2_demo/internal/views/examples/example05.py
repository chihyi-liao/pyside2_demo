from PySide2.QtCore import Slot, Qt
from PySide2.QtWidgets import (
    QMainWindow,  QWidget, QGridLayout, QHBoxLayout, QPushButton, QTabWidget, QMessageBox)

from pyside2_demo.internal.views.common import QHLine


class TabWidget(QWidget):
    def __init__(self):
        super(TabWidget, self).__init__()


class HelpCornerWidget(QWidget):
    def __init__(self, parent=None):
        super(HelpCornerWidget, self).__init__(parent)
        layout = QHBoxLayout()
        help_btn = QPushButton("?")
        help_btn.setFixedWidth(30)
        help_btn.clicked.connect(self.help_btn_fn)
        layout.addWidget(help_btn)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    @Slot()
    def help_btn_fn(self):
        msg = QMessageBox(QMessageBox.NoIcon, '幫助', '幫助說明')
        msg.exec_()


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        tab_main = QTabWidget()
        tab_main.addTab(TabWidget(), "Main")
        tab_main.addTab(TabWidget(), "Settings")
        tab_main.setCornerWidget(HelpCornerWidget(self), Qt.TopRightCorner)
        tab_main.setTabBarAutoHide(True)
        tab_main.currentChanged.connect(self.tab_bar_changed_fn)
        line = QHLine()
        add_btn = QPushButton("&Add")
        add_btn.clicked.connect(self.add_btn_fn)
        add_btn.setFixedWidth(100)
        del_btn = QPushButton("&Delete")
        del_btn.clicked.connect(self.del_btn_fn)
        del_btn.setFixedWidth(100)
        # 設定 layout
        layout = QGridLayout()
        layout.addWidget(tab_main, 0, 0, 1, 3)
        layout.addWidget(line, 1, 0, 1, 3)
        layout.addWidget(del_btn, 2, 1)
        layout.addWidget(add_btn, 2, 2)
        self.tab_main = tab_main
        self.setLayout(layout)

    @Slot()
    def add_btn_fn(self):
        count = self.tab_main.count()
        self.tab_main.insertTab(count, TabWidget(), "Tab%d" % (count-1, ))

    @Slot()
    def del_btn_fn(self):
        count = self.tab_main.count()
        if count > 2:
            self.tab_main.removeTab(count-1)

    @Slot()
    def tab_bar_changed_fn(self):
        idx = self.tab_main.currentIndex()
        if idx != -1:
            tab_text = self.tab_main.tabText(idx)
            msg = QMessageBox(QMessageBox.NoIcon, 'Tab', 'Current Tab is %s' % (tab_text, ))
            msg.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Example04")
        self.resize(600, 400)
