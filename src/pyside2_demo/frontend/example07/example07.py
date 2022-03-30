try:
    import matplotlib
    import mplfinance as mpf
    from mplfinance._arg_validators import _get_valid_plot_types  # noqa
    matplotlib.use('Qt5Agg')
except ImportError:
    raise

import pandas as pd

from PySide2.QtCore import Slot, Qt, QEvent
from PySide2.QtWidgets import (
    QMainWindow,  QWidget, QGridLayout, QPushButton, QLabel, QComboBox,
    QGroupBox, QSpinBox, QVBoxLayout, QSizePolicy, QDoubleSpinBox, QCheckBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib import pyplot as plt

from pyside2_demo.backend import compute
from pyside2_demo.common import QHLine
from pyside2_demo.utils import get_resource


MyFont = FontProperties(fname=get_resource('NotoSansTC-Medium.otf'))
MyData = pd.read_csv(get_resource('tw-2330.csv'), index_col=0, parse_dates=True)
MyData.index.name = 'Date'


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, fig=None, axes=None):
        if fig is None:
            self.fig = Figure()
            self.axes = self.fig.subplots()
        else:
            self.fig = fig
            self.axes = axes
        super(MplCanvas, self).__init__(fig)


class MpfStockWidget(QWidget):
    def __init__(self):
        super(MpfStockWidget, self).__init__()
        layout = QVBoxLayout()
        canvas = MplCanvas()
        layout.addWidget(canvas)
        self.setLayout(layout)
        self.canvas = canvas
        self.data = pd.DataFrame()

    def draw(self, params: dict):
        layout = self.layout()
        if self.canvas:
            layout.removeWidget(self.canvas)
            if isinstance(self.canvas.axes, list):
                plt.cla()
                plt.clf()
                plt.close()
            else:
                self.canvas.axes.cla()
                self.canvas.fig.clf()

        days = params['days']
        self.data = MyData.iloc[-days:, :]
        mpf_params = params['mplfinance']
        hlines = []
        if mpf_params["enable_hlines"]:
            co_values = self.data['Close']
            co_max = co_values.max()
            co_min = co_values.min()
            lo_line = (co_max - co_min) * 0.2 + co_min
            hi_line = (co_max - co_min) * 0.8 + co_min
            hlines = dict(hlines=[lo_line, hi_line], colors=['b', 'r'], linestyle='-.', linewidths=(1, 1))

        s, m, d = compute.macd(self.data['Close'])
        ap2 = [mpf.make_addplot(s, color='yellow', panel=2),
               mpf.make_addplot(m, color='g', panel=2),
               mpf.make_addplot(d, type='bar', color='dimgray', panel=2, alpha=1)]

        tw_colors = mpf.make_marketcolors(up='r', down='g', inherit=True)
        style = mpf.make_mpf_style(base_mpf_style=mpf_params['style'], marketcolors=tw_colors, y_on_right=False)
        fig, axes = mpf.plot(data=self.data, style=style, type=mpf_params['type'], hlines=hlines,
                             mav=mpf_params['mav'], returnfig=True, volume=mpf_params['volume'],
                             figscale=mpf_params['figscale'], fontscale=mpf_params['fontscale'],
                             ylabel='', datetime_format="%d\n%b", tight_layout=mpf_params['tight_layout'],
                             addplot=ap2, xrotation=0)

        # panel label settings, a panel will take 2 axes
        main_panel = mpf_params.get('main_panel', 0)
        axes[main_panel*2].set_ylabel('股價', fontproperties=MyFont, fontsize=8)
        volume = mpf_params['volume']
        if volume:
            volume_panel = mpf_params.get('volume_panel', 1)
            axes[volume_panel*2].set_ylabel('成交量', fontproperties=MyFont, fontsize=8)

        # set title on top of panels
        title = "{name}({code})".format(name=params['name'], code=params['code'])
        axes[0].set_title(title, fontproperties=MyFont, fontsize=8, loc='right')

        self.canvas = MplCanvas(fig, axes)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        layout.addWidget(self.canvas)

    @Slot(QEvent)
    def on_motion(self, event):
        if event.xdata and event.xdata > 0:
            x = int(event.xdata + 0.5)
            if x <= self.data.shape[0]-1:
                data = self.data.iloc[x]
                date_str = pd.to_datetime(data.name, format='%Y-%m-%d').strftime('%y-%m-%d')
                msg = "日期:{date}\n開盤:{open}  最高:{high}  最低:{low}  收盤:{close}  量:{volume}".format(
                    date=date_str, open=data['Open'], high=data['High'],
                    low=data['Low'], close=data['Close'], volume=int(data['Volume']))
                self.canvas.axes[0].set_title(msg, fontproperties=MyFont, fontsize=8, loc='left')
                self.canvas.draw()


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        # initial widget
        code_label = QLabel("Code")
        code_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        code_combox = QComboBox()
        code_combox.addItems(["2330"])
        name_label = QLabel("Name")
        name_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        name_combox = QComboBox()
        name_combox.addItems(["台積電"])
        data_days_label = QLabel("Days")
        data_days_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        data_days_spin_box = QSpinBox()
        data_days_spin_box.setMinimum(1)
        data_days_spin_box.setMaximum(MyData.shape[0])
        data_days_spin_box.setValue(100)

        # mpf params widgets
        style_label = QLabel("Style")
        style_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        style_combox = QComboBox()
        style_combox.addItems(mpf.available_styles())
        type_label = QLabel("Type")
        type_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        type_combox = QComboBox()
        type_combox.addItems(_get_valid_plot_types())
        volume_label = QLabel("Volume")
        volume_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        volume_combox = QComboBox()
        volume_combox.addItems(["False", "True"])
        volume_combox.setCurrentIndex(1)

        tight_layout_label = QLabel("Tight Layout")
        tight_layout_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        tight_layout_combox = QComboBox()
        tight_layout_combox.addItems(["False", "True"])
        tight_layout_combox.setCurrentIndex(0)

        fig_scale_label = QLabel("Fig Scale")
        fig_scale_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        fig_scale_spin_box = QDoubleSpinBox()
        fig_scale_spin_box.setMinimum(0.1)
        fig_scale_spin_box.setMaximum(2.0)
        fig_scale_spin_box.setSingleStep(0.05)
        fig_scale_spin_box.setValue(1.0)

        font_scale_label = QLabel("Font Scale")
        font_scale_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        font_scale_spin_box = QDoubleSpinBox()
        font_scale_spin_box.setMinimum(0.1)
        font_scale_spin_box.setMaximum(2.0)
        font_scale_spin_box.setSingleStep(0.05)
        font_scale_spin_box.setValue(0.65)

        h_line_label = QLabel("HLine")
        h_line_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        h_line_chk_box = QCheckBox()
        h_line_chk_box.setChecked(False)

        ma5_label = QLabel("MA5")
        ma5_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        ma5_chk_box = QCheckBox()
        ma5_chk_box.setChecked(True)
        ma10_label = QLabel("MA10")
        ma10_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        ma10_chk_box = QCheckBox()
        ma10_chk_box.setChecked(True)
        ma20_label = QLabel("MA20")
        ma20_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        ma20_chk_box = QCheckBox()
        ma20_chk_box.setChecked(True)

        # set group layout
        group = QGroupBox("Params")
        group_layout = QGridLayout()
        group_layout.addWidget(code_label, 0, 0)
        group_layout.addWidget(code_combox, 0, 1)
        group_layout.addWidget(name_label, 0, 2)
        group_layout.addWidget(name_combox, 0, 3)
        group_layout.addWidget(data_days_label, 0, 4)
        group_layout.addWidget(data_days_spin_box, 0, 5)
        group_layout.addWidget(type_label, 1, 0)
        group_layout.addWidget(type_combox, 1, 1)
        group_layout.addWidget(style_label, 1, 2)
        group_layout.addWidget(style_combox, 1, 3)
        group_layout.addWidget(volume_label, 1, 4)
        group_layout.addWidget(volume_combox, 1, 5)
        group_layout.addWidget(tight_layout_label, 1, 6)
        group_layout.addWidget(tight_layout_combox, 1, 7)
        group_layout.addWidget(h_line_label, 1, 8)
        group_layout.addWidget(h_line_chk_box, 1, 9)

        group_layout.addWidget(fig_scale_label, 2, 0)
        group_layout.addWidget(fig_scale_spin_box, 2, 1)
        group_layout.addWidget(font_scale_label, 2, 2)
        group_layout.addWidget(font_scale_spin_box, 2, 3)
        group_layout.addWidget(ma5_label, 2, 4)
        group_layout.addWidget(ma5_chk_box, 2, 5)
        group_layout.addWidget(ma10_label, 2, 6)
        group_layout.addWidget(ma10_chk_box, 2, 7)
        group_layout.addWidget(ma20_label, 2, 8)
        group_layout.addWidget(ma20_chk_box, 2, 9)
        group.setLayout(group_layout)
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        mpf_stock = MpfStockWidget()
        mpf_stock.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        execute_btn = QPushButton("Execute")
        execute_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        execute_btn.clicked.connect(self.execute_btn_fn)

        layout = QGridLayout()
        layout.addWidget(group, 0, 0, 1, 2)
        layout.addWidget(QHLine(), 1, 0, 1, 2)
        layout.addWidget(execute_btn, 2, 1)
        layout.addWidget(mpf_stock, 3, 0, 1, 2)
        self.setLayout(layout)

        # attachment control widget
        self.code_combox = code_combox
        self.name_combox = name_combox
        self.data_days_spin_box = data_days_spin_box
        self.style_combox = style_combox
        self.type_combox = type_combox
        self.volume_combox = volume_combox
        self.tight_layout_combox = tight_layout_combox
        self.fig_scale_spin_box = fig_scale_spin_box
        self.font_scale_spin_box = font_scale_spin_box
        self.ma5_chk_box = ma5_chk_box
        self.ma10_chk_box = ma10_chk_box
        self.ma20_chk_box = ma20_chk_box
        self.h_line_chk_box = h_line_chk_box
        self.mpf_stock = mpf_stock

    def get_params(self):
        mav = []
        if self.ma5_chk_box.isChecked():
            mav.append(5)

        if self.ma10_chk_box.isChecked():
            mav.append(10)

        if self.ma20_chk_box.isChecked():
            mav.append(20)

        return {
            'code': self.code_combox.currentText(), 'name':  self.name_combox.currentText(),
            'days': self.data_days_spin_box.value(),
            'mplfinance': {
                'style': self.style_combox.currentText(), 'type': self.type_combox.currentText(),
                'volume': True if self.volume_combox.currentText() == 'True' else False,
                'tight_layout': True if self.tight_layout_combox.currentText() == 'True' else False,
                'figscale': self.fig_scale_spin_box.value(), 'fontscale': self.font_scale_spin_box.value(),
                'mav': tuple(mav), 'enable_hlines': self.h_line_chk_box.isChecked()
            }
        }

    @Slot()
    def execute_btn_fn(self):
        self.mpf_stock.draw(params=self.get_params())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Example07")
        self.resize(1024, 720)
