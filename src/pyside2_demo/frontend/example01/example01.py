from PySide2.QtCore import Slot, Qt, QThreadPool, QCoreApplication, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QDialog, QLabel, QLineEdit, QComboBox, QMainWindow, QMessageBox,
    QWidget, QPushButton, QGridLayout, QDialogButtonBox, QTextEdit,
)

from pyside2_demo.utils import get_resource
from pyside2_demo.common import is_valid_user, Worker


EditLineStyleSheet = """QLineEdit{ 
                          background-color:rgb(202, 255, 227);
                          border: 2px solid gray;
                          padding: 0 8px;
                          selection-background-color: darkgray;
                          font-size: 16px;}
                          QLineEdit: focus { 
                          background-color:rgb(192, 192, 255);}"""


class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()
        # 初始化圖形控件
        region_label = QLabel("地區")
        combox = QComboBox()
        combox.addItems(["台北", "台中", "高雄"])
        username_label = QLabel("用戶名稱")
        username_line = QLineEdit()
        username_line.setStyleSheet(EditLineStyleSheet)
        username_line.setText("admin")
        passwd_label = QLabel("密碼")
        passwd_line = QLineEdit()
        passwd_line.setText("password")
        passwd_line.setEchoMode(QLineEdit.Password)
        passwd_line.setStyleSheet(EditLineStyleSheet)
        status_label = QLabel()
        status_label.setAlignment(Qt.AlignCenter)
        dialog_btn_box = QDialogButtonBox()
        dialog_btn_box.addButton(QDialogButtonBox.Ok)
        dialog_btn_box.addButton(QDialogButtonBox.Cancel)
        dialog_btn_box.accepted.connect(self.execute_login_job)
        dialog_btn_box.rejected.connect(self.reject)
        # 設定 layout
        layout = QGridLayout()
        layout.addWidget(username_label, 0, 0)
        layout.addWidget(username_line, 0, 1)
        layout.addWidget(passwd_label, 1, 0)
        layout.addWidget(passwd_line, 1, 1)
        layout.addWidget(region_label, 2, 0)
        layout.addWidget(combox, 2, 1)
        layout.addWidget(status_label, 3, 0, 1, 2)
        layout.addWidget(dialog_btn_box, 4, 0, 1, 2)
        # 內嵌圖形控件
        self.username_line = username_line
        self.passwd_line = passwd_line
        self.status_label = status_label
        # 設定 widget 參數
        self.setLayout(layout)
        self.setWindowTitle("登入")
        self.setFixedSize(250, 250)

    @Slot()
    def execute_login_job(self):
        threads = QThreadPool()
        worker = Worker(self.login_job)
        worker.signals.progress.connect(self.login_progress)
        worker.signals.result.connect(self.login_result)
        worker.signals.finished.connect(self.login_finished)
        threads.start(worker)

    def login_job(self, progress_callback):
        progress_callback.emit(100)
        status = is_valid_user(self.username_line.text(), self.passwd_line.text())
        return status

    @Slot(int)
    def login_progress(self, _):
        self.status_label.setText("登入中")

    @Slot(bool)
    def login_result(self, status):
        if status is True:
            self.status_label.setText("成功")
            self.accept()
        else:
            self.status_label.setText("名稱或是密碼不正確")

    @Slot()
    def login_finished(self):
        return


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        # 初始化圖形控件
        animation_label = QLabel("片名")
        combox = QComboBox()
        combox.addItems(["你的名字", "天氣之子", "隱瞞之事", "鬼滅之刃"])
        combox.currentTextChanged.connect(self.text_changed)
        title_label = QLabel("Title")
        message_line = QLineEdit()
        message_line.setText("message title")
        message_button = QPushButton("Send Msg")
        message_label = QLabel("Message")
        message_label.setAlignment(Qt.AlignTop)
        message_label.setFixedSize(message_label.sizeHint())  # 避免message_label控件被延展
        message_edit = QTextEdit("input Message")
        message_edit.setAlignment(Qt.AlignTop)
        exit_button = QPushButton("Exit")
        exit_button.setIcon(QIcon(get_resource('exit.png')))
        exit_button.setIconSize(QSize(20, 20))
        exit_button.clicked.connect(QCoreApplication.instance().quit)
        # 設定 layout
        layout = QGridLayout()
        layout.addWidget(animation_label, 0, 0)
        layout.addWidget(combox, 0, 1)
        layout.addWidget(title_label, 1, 0)
        layout.addWidget(message_line, 1, 1)
        layout.addWidget(message_label, 2, 0)
        layout.addWidget(message_edit, 3, 0, 3, 2)
        layout.addWidget(message_button, 4, 2)
        layout.addWidget(exit_button, 5, 2)

        # 設定 widget 參數
        self.message_line = message_line
        self.setLayout(layout)

    @Slot()
    def text_changed(self, s: str):
        msg = "[%s]: Title" % (s, )
        self.message_line.setText(msg)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Example01")
        self.resize(600, 400)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "關閉程式", '是否關閉程式?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
