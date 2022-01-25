try:
    import matplotlib
    matplotlib.use('Qt5Agg')
except ImportError:
    raise

import random
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QMainWindow,  QWidget, QGridLayout, QPushButton)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties

from pyside2_demo.internal.utils import get_resource

font = FontProperties(fname=get_resource('NotoSansTC-Medium.otf'))


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.subplots()
        super(MplCanvas, self).__init__(fig)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.canvas = MplCanvas()

        btn = QPushButton("OK")
        btn.clicked.connect(self.btn_fn)
        # 設定 layout
        layout = QGridLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(btn)
        self.setLayout(layout)

    @Slot()
    def btn_fn(self):
        self.canvas.axes.cla()
        data = []
        x = []
        for i in range(100):
            x.append(i)
            data.append(random.randint(10, 50))
        self.canvas.axes.set_title("測試(test)", fontproperties=font, fontsize=12)
        self.canvas.axes.set_xlabel("0-100", fontproperties=font, fontsize=8)
        self.canvas.axes.set_ylabel("10-50", fontproperties=font, fontsize=8)
        self.canvas.axes.plot(x, data)
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Example06")
        self.resize(600, 400)
