from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QFont
from PySide2.QtWidgets import (
    QLabel, QMainWindow,  QWidget, QGridLayout, QTextEdit, QGroupBox, QHBoxLayout, QVBoxLayout)

from pyside2_demo.internal.utils import get_resource
from pyside2_demo.internal.views.common import set_widget_on_screen_center, draw_sketch, RoundAvatar


class HeaderSubWidget(QWidget):
    def __init__(self):
        super(HeaderSubWidget, self).__init__()
        layout = QHBoxLayout()
        self.setFixedHeight(200)
        # group1 設定
        group1 = QGroupBox()
        group1.setTitle("封面")
        group1_layout = QGridLayout()
        avatar_label = RoundAvatar(filepath=get_resource('ex02-01.jpeg'), avatar_size=150)
        name_label = QLabel("皮在楊")
        name_label.setFont(QFont('Arial', 24))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: red;")
        title_label = QLabel("現職: 應屆畢業生")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: yellow;")
        group1_layout.addWidget(avatar_label, 0, 0, 2, 1)
        group1_layout.addWidget(name_label, 0, 1)
        group1_layout.addWidget(title_label, 1, 1)
        group1_layout.setRowStretch(0, 2)
        group1_layout.setRowStretch(1, 1)
        group1.setLayout(group1_layout)
        group1.setStyleSheet("""
                             QLabel{color: white; background-color: rgba(255, 255, 255, 0);}
                             QGroupBox{
                                 background-color: rgba(90, 135, 160, 255);
                             }
                             QGroupBox:title {
                                 color: rgba(255, 255, 255, 0);
                                 background-color: rgba(90, 135, 160, 255);
                             };""")

        # group2 設定
        group2 = QGroupBox()
        group2.setTitle("基本資料")
        group2_layout = QVBoxLayout()
        phone_label = QLabel("電話: 09xx-xxx-xxx")
        email_label = QLabel("信箱: user@example.com")
        address_label = QLabel("地址: 台北市中山區林森北路9號")
        education_label = QLabel("學歷: 碩士")
        group2_layout.addWidget(phone_label)
        group2_layout.addWidget(email_label)
        group2_layout.addWidget(address_label)
        group2_layout.addWidget(education_label)
        group2.setLayout(group2_layout)
        group2.setStyleSheet("""
                             QLabel{color: white; background-color: rgba(255, 255, 255, 0);}
                             QGroupBox{
                                 background-color: rgba(0, 90, 140, 255);
                             }
                             QGroupBox:title {
                                 color: rgba(255, 255, 255, 0);
                                 background-color: rgba(0, 90, 140, 255);
                             };""")

        layout.addWidget(group1)
        layout.addWidget(group2)
        layout.setStretch(0, 2)
        layout.setStretch(1, 1)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.name_label = name_label
        self.title_label = title_label
        self.group1_layout = group1_layout
        self.group2_layout = group2_layout
        self.group1 = group1
        self.group2 = group2
        self.layout = layout
        self.setLayout(layout)

    def paintEvent(self, e):
        painter = QPainter(self)
        draw_sketch(painter, self.name_label.x(), self.name_label.y(),
                    self.name_label.width(), self.name_label.height(), color=Qt.red, brush=2)

        draw_sketch(painter, self.title_label.x(), self.title_label.y(),
                    self.title_label.width(), self.title_label.height(), color=Qt.blue, brush=2)


class ContentSubWidget(QWidget):
    def __init__(self):
        super(ContentSubWidget, self).__init__()
        self.setStyleSheet("background-color: rgba(113, 124, 121, 255);")
        content1 = QLabel("教育背景")
        content1.setAlignment(Qt.AlignHCenter)
        content1.setFont(QFont('Arial', 24))
        content1.setStyleSheet("QLabel{color: black; background-color: rgba(255, 255, 255, 0);}")
        content2 = QLabel("專業技能")
        content2.setAlignment(Qt.AlignHCenter)
        content2.setFont(QFont('Arial', 24))
        content2.setStyleSheet("QLabel{color: black; background-color: rgba(255, 255, 255, 0);}")
        text_edit = QTextEdit()
        text_edit.setHtml("""
        <body>
          <p><span style="color:blue">怪獸電力大學 電機學院</span></p>
          <p><span style="color:blue">電力工程系 學士</span> GPA3.6/4.0 排名 3/16</p>
          <p><span style="color:blue">怪獸電力大學 電機學院</span></p>  
          <p><span style="color:blue">電力工程系 碩士</span> GPA3.6/4.0 排名 3/16</p>  
        </body>
        """)
        text_edit.setReadOnly(True)
        text_edit2 = QTextEdit()
        text_edit2.setReadOnly(True)
        text_edit2.setHtml("""
        <body>
          <p><span style="color:blue">C/C++<span></p>
          <p><span style="color:blue">Python2/Python3<span></p>
          <p><span style="color:blue">Javascript<span></p>
        </body>
        """)
        layout = QGridLayout()
        layout.addWidget(content1, 0, 0)
        layout.addWidget(text_edit, 0, 1)
        layout.addWidget(content2, 1, 0)
        layout.addWidget(text_edit2, 1, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 5)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        # 初始化圖形控件
        header = HeaderSubWidget()
        content = ContentSubWidget()
        # 設定 layout
        layout = QGridLayout()
        layout.addWidget(header, 0, 0)
        layout.addWidget(content, 1, 0)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # 設定 widget 參數
        self.layout = layout
        self.header = header
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        set_widget_on_screen_center(self, 1024, 768)
        self.init_status_bar()
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Example02")

    def init_status_bar(self):
        status_bar = self.statusBar()
        status_bar.showMessage('Ready')
