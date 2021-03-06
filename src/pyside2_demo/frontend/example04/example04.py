from PySide2.QtCore import Slot, Qt
from PySide2.QtWidgets import (
    QMainWindow,  QWidget, QGridLayout, QVBoxLayout,  QLabel, QHeaderView, QAbstractItemView,
    QLineEdit, QPushButton, QSplitter, QTableWidget, QTableWidgetItem, QGroupBox)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        splitter = QSplitter(Qt.Vertical)
        top_layout = QGridLayout()

        # 設定group
        group = QGroupBox("基本資料")
        group_layout = QGridLayout()
        name_label = QLabel("名稱")
        name_line = QLineEdit()
        name_line.setPlaceholderText("皮在楊")
        email_label = QLabel("信箱")
        email_line = QLineEdit()
        email_line.setPlaceholderText("user@example.com")
        address_label = QLabel("住址")
        address_line = QLineEdit()
        address_line.setPlaceholderText("台北市中山區林森北路9號")
        phone_label = QLabel("電話")
        phone_line = QLineEdit()
        phone_line.setPlaceholderText("09xx-xxx-xxx")
        group_layout.addWidget(name_label, 0, 0)
        group_layout.addWidget(name_line, 0, 1)
        group_layout.addWidget(email_label, 0, 2)
        group_layout.addWidget(email_line, 0, 3)
        group_layout.addWidget(address_label, 1, 0)
        group_layout.addWidget(address_line, 1, 1)
        group_layout.addWidget(phone_label, 1, 2)
        group_layout.addWidget(phone_line, 1, 3)
        group.setLayout(group_layout)

        # 設定 table
        table = QTableWidget(0, 4)
        table.cellClicked.connect(self.table_cell_clicked_fn)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 點選時會包含整個row
        table.setHorizontalHeaderItem(0, QTableWidgetItem(name_label.text()))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(email_label.text()))
        table.setHorizontalHeaderItem(2, QTableWidgetItem(address_label.text()))
        table.setHorizontalHeaderItem(3, QTableWidgetItem(phone_label.text()))
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        splitter.addWidget(group)
        splitter.addWidget(table)

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_btn_fn)
        update_btn = QPushButton("Update")
        update_btn.clicked.connect(self.update_btn_fn)
        update_btn.setDisabled(True)
        del_btn = QPushButton("Delete")
        del_btn.clicked.connect(self.del_btn_fn)
        del_btn.setDisabled(True)
        top_layout.addWidget(splitter, 0, 0, 1, 4)
        top_layout.addWidget(del_btn, 1, 1)
        top_layout.addWidget(update_btn, 1, 2)
        top_layout.addWidget(add_btn, 1, 3)

        # 設定 layout
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        # 設定 widget 參數
        self.name_line = name_line
        self.email_line = email_line
        self.address_line = address_line
        self.phone_line = phone_line
        self.table = table
        self.update_btn = update_btn
        self.del_btn = del_btn
        self.setLayout(layout)

    @Slot()
    def add_btn_fn(self):
        row = self.table.rowCount()
        name = self.name_line.text()
        email = self.email_line.text()
        address = self.address_line.text()
        phone = self.phone_line.text()
        if name and email and address and phone:
            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)  # item 改成唯讀
            email_item = QTableWidgetItem(email)
            email_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)  # item 改成唯讀
            address_item = QTableWidgetItem(address)
            address_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)  # item 改成唯讀
            phone_item = QTableWidgetItem(phone)
            phone_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)  # item 改成唯讀
            self.table.insertRow(row)
            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, email_item)
            self.table.setItem(row, 2, address_item)
            self.table.setItem(row, 3, phone_item)
            self.update_btn.setEnabled(True)
            self.del_btn.setEnabled(True)

    @Slot()
    def update_btn_fn(self):
        row = self.table.currentRow()
        if row != -1:
            name = self.name_line.text()
            email = self.email_line.text()
            address = self.address_line.text()
            phone = self.phone_line.text()
            if name and email and address and phone:
                name_item = QTableWidgetItem(name)
                name_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)  # item 改成唯讀
                email_item = QTableWidgetItem(email)
                email_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)  # item 改成唯讀
                address_item = QTableWidgetItem(address)
                address_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)  # item 改成唯讀
                phone_item = QTableWidgetItem(phone)
                phone_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)  # item 改成唯讀
                self.table.setItem(row, 0, name_item)
                self.table.setItem(row, 1, email_item)
                self.table.setItem(row, 2, address_item)
                self.table.setItem(row, 3, phone_item)

    @Slot()
    def del_btn_fn(self):
        idx = self.table.currentRow()
        if idx != -1:
            self.table.removeRow(idx)

        if not self.table.rowCount():
            self.update_btn.setDisabled(True)
            self.del_btn.setDisabled(True)

    @Slot()
    def table_cell_clicked_fn(self):
        row = self.table.currentRow()
        map_line = {
            0: self.name_line, 1: self.email_line,
            2: self.address_line, 3: self.phone_line}
        for col in range(self.table.columnCount()):
            line = map_line.get(col)
            if line:
                item = self.table.item(row, col)
                line.setText(item.text())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Example04")
        self.resize(600, 400)
