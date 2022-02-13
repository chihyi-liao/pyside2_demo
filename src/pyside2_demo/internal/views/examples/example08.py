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
    QGroupBox, QVBoxLayout, QSizePolicy)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.font_manager import FontProperties
from pyside2_demo.internal import compute
from pyside2_demo.internal.views.common import QHLine
from pyside2_demo.internal.utils import get_resource


MyStyle = dict(
    style_name='mike',
    base_mpf_style='mike',
    base_mpl_style='dark_background',
    marketcolors={
        'candle': {'up': '#ff0000', 'down': '#00ff00'},
        'edge': {'up': '#ff0000', 'down': '#00ff00'},
        'wick': {'up': '#ff0000', 'down': '#00ff00'},
        'ohlc': {'up': '#ff0000', 'down': '#00ff00'},
        'volume': {'up': '#ff0000', 'down': '#00ff00'},
        'vcdopcod': False,  # Volume Color Depends On Price Change On Day
        'alpha': 1.0},
    mavcolors=['#ec009c', '#78ff8f', '#fcf120'],
    y_on_right=False,
    gridcolor=None,
    gridstyle=None,
    facecolor=None,
    rc=[
        ('axes.edgecolor', 'white'),
        ('axes.linewidth', 1.5),
        ('axes.labelsize', 'large'),
        ('axes.labelweight', 'semibold'),
        ('axes.grid', True),
        ('axes.grid.axis', 'both'),
        ('axes.grid.which', 'major'),
        ('grid.alpha',  0.5),
        ('grid.color', '#b0b0b0'),
        ('grid.linestyle', '--'),
        ('grid.linewidth',  0.8),
        ('figure.facecolor', '#0a0a0a'),
        ('patch.linewidth',  1.0),
        ('lines.linewidth',  1.0),
        ('font.weight', 'medium'),
        ('font.size',  8.0),
        ('figure.titlesize', 'x-large'),
        ('figure.titleweight', 'semibold'),
    ]
)
MyFont = FontProperties(fname=get_resource('NotoSansTC-Medium.otf'))
MyData = pd.read_csv(get_resource('tw-2330.csv'), parse_dates=['Date'])
MyFontParams = {'fontproperties': MyFont, 'fontsize': 8}


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = mpf.figure(style=MyStyle)
        self.axes = []
        super(MplCanvas, self).__init__(self.fig)

    def add_axes(self, *args, **kwargs):
        self.axes.append(self.fig.add_axes(*args, **kwargs))


class MpfStockWidget(QWidget):
    def __init__(self, data: pd.DataFrame, view_num: int = 100, enable_extra_ax: bool = False):
        super(MpfStockWidget, self).__init__()
        canvas = MplCanvas()
        canvas.add_axes([0.08, 0.25, 0.88, 0.65])
        canvas.add_axes([0.08, 0.15, 0.88, 0.1], sharex=canvas.axes[0])
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.setLayout(layout)
        self.data = data
        self.aps = []
        self.main_ax = canvas.axes[0]
        self.main_ax_vertical_line = self.main_ax.axvline(color='#d49424', linewidth=1, linestyle="-")
        if enable_extra_ax:
            canvas.add_axes([0.08, 0.05, 0.88, 0.1], sharex=canvas.axes[0])
            self.extra_ax = canvas.axes[1]
            self.extra_ax_vertical_line = self.extra_ax.axvline(color='#d49424', linewidth=1, linestyle="-")
            self.extra_ax_ylabel = ''
            self.volume_ax = canvas.axes[2]
            self.volume_ax_vertical_line = self.volume_ax.axvline(color='#d49424', linewidth=1, linestyle="-")
        else:
            self.extra_ax = None
            self.extra_ax_vertical_line = None
            self.extra_ax_ylabel = None
            self.volume_ax = canvas.axes[1]
            self.volume_ax_vertical_line = self.volume_ax.axvline(color='#d49424', linewidth=1, linestyle="-")

        self.mouse_press = False
        self.mouse_xpress = None
        max_x = data.shape[0] - 1
        if view_num > max_x:
            self.view_num = max_x
            self.idx_start = 0
        else:
            self.view_num = view_num
            self.idx_start = max_x - self.view_num

        self.canvas = canvas
        self.canvas_bind_event_flag = False

        # Init Canvas Text
        self.name_text = self.canvas.fig.text(0.08, 0.95, '台積電 (2330)', **MyFontParams)
        self.date_text = self.canvas.fig.text(0.08, 0.92, '日期:', **MyFontParams)
        self.open_title_text = self.canvas.fig.text(0.20, 0.95, '開盤:', **MyFontParams)
        self.open_value_text = self.canvas.fig.text(0.23, 0.95, '', **MyFontParams)
        self.close_title_text = self.canvas.fig.text(0.20, 0.92, '收盤:', **MyFontParams)
        self.close_value_text = self.canvas.fig.text(0.23, 0.92, '', **MyFontParams)
        self.high_title_text = self.canvas.fig.text(0.28, 0.95, '最高:', **MyFontParams)
        self.high_value_text = self.canvas.fig.text(0.31, 0.95, '', **MyFontParams)
        self.low_title_text = self.canvas.fig.text(0.28, 0.92, '最低:', **MyFontParams)
        self.low_value_text = self.canvas.fig.text(0.31, 0.92, '', **MyFontParams)
        self.change_title_text = self.canvas.fig.text(0.36, 0.95, '漲幅:', **MyFontParams)
        self.change_value_text = self.canvas.fig.text(0.39, 0.95, '', **MyFontParams)
        self.volume_title_text = self.canvas.fig.text(0.36, 0.92, '總量:', **MyFontParams)
        self.volume_value_text = self.canvas.fig.text(0.39, 0.92, '', **MyFontParams)

    def reset(self):
        self.clear_axes()
        self.canvas.fig.clf()
        self.aps = []
        self.canvas_bind_event_flag = False
        self.mouse_press = False
        self.mouse_xpress = None
        self.view_num = 100
        if self.view_num > self.data.shape[0] - 1:
            self.view_num = self.data.shape[0] - 1
            self.idx_start = 0
        else:
            self.idx_start = self.data.shape[0] - 1 - self.view_num

    def clear_axes(self):
        for ax in self.canvas.axes:
            ax.clear()

    def set_main_ax_addplot(self, columns: list = None, columns_params: list = None):
        if not columns or not columns_params:
            return

        if len(columns) != len(columns_params):
            return

        for col, params in zip(columns, columns_params):
            params['ax'] = self.main_ax
            self.aps.append(tuple([col, params]))

    def set_extra_ax_addplot(self, columns: list = None, columns_params: list = None, ylabel: str = 'Extra'):
        if not columns or not columns_params:
            return

        if len(columns) != len(columns_params):
            return

        if self.extra_ax:
            self.extra_ax_ylabel = ylabel
            for col, params in zip(columns, columns_params):
                params['ax'] = self.extra_ax
                self.aps.append(tuple([col, params]))

    @Slot(QEvent)
    def on_scroll(self, event):
        if not event.inaxes == self.main_ax:
            return

        idx_start = self.idx_start
        max_x = self.data.shape[0] - 1
        if event.button == 'down':
            view_num = 100 if self.view_num - 50 < 100 else self.view_num - 50
        elif event.button == 'up':
            view_num = 400 if self.view_num + 50 > 400 else self.view_num + 50
        else:
            return

        if max_x - view_num > 0:
            if idx_start+view_num > max_x:
                idx_start = max_x - view_num
        else:
            idx_start = 0
            view_num = max_x

        if view_num == self.view_num:
            return

        self.idx_start = idx_start
        self.view_num = view_num
        self.refresh_plot(idx_start=self.idx_start, view_num=self.view_num)

    @Slot(QEvent)
    def on_press(self, event):
        if not event.inaxes == self.main_ax:
            return

        # check left mouse is clicked
        if event.button != 1:
            return

        self.mouse_press = True
        if event.xdata:
            x = int(event.xdata + 0.5)
            max_x = self.data.shape[0] - 1
            if x <= max_x:
                self.mouse_xpress = x

        self.main_ax_vertical_line.set_visible(False)
        self.volume_ax_vertical_line.set_visible(False)
        if self.extra_ax:
            self.extra_ax_vertical_line.set_visible(False)
        self.canvas.draw()

    @Slot(QEvent)
    def on_release(self, event):
        self.mouse_press = False
        if not event.inaxes == self.main_ax:
            return

        if event.xdata:
            x = int(event.xdata + 0.5)
            max_x = self.data.shape[0] - 1
            if x <= max_x:
                self.idx_start -= int(event.xdata - self.mouse_xpress)
                if self.idx_start < 0:
                    self.idx_start = 0
                elif self.idx_start >= max_x - self.view_num:
                    self.idx_start = max_x - self.view_num
                self.refresh_plot(idx_start=self.idx_start, view_num=self.view_num)

    @Slot(QEvent)
    def on_motion(self, event):
        if self.mouse_press:
            return

        if not event.inaxes == self.main_ax:
            return

        if event.xdata:
            x = int(event.xdata + 0.5)
            if self.idx_start-1 < x+self.idx_start <= self.data.shape[0]-1:
                data = self.data.iloc[x+self.idx_start]
                self.main_ax_vertical_line.set_xdata(x)
                self.volume_ax_vertical_line.set_xdata(x)
                if self.extra_ax:
                    self.extra_ax_vertical_line.set_xdata(x)
                self.refresh_text(data)
                self.canvas.draw()

    def refresh_text(self, data: pd.DataFrame):
        date_str = pd.to_datetime(data.name, format='%Y-%m-%d').strftime('%y-%m-%d')
        red = '#ff0000'
        green = '#00ff00'
        white = '#ffffff'
        change = data['Change']
        prev_price = data['Close'] - change

        if data['Open'] > prev_price:
            self.open_value_text.set_color(red)
        elif data['Open'] < prev_price:
            self.open_value_text.set_color(green)
        else:
            self.open_value_text.set_color(white)

        if data['High'] > prev_price:
            self.high_value_text.set_color(red)
        elif data['High'] < prev_price:
            self.high_value_text.set_color(green)
        else:
            self.high_value_text.set_color(white)

        if data['Low'] > prev_price:
            self.low_value_text.set_color(red)
        elif data['Low'] < prev_price:
            self.low_value_text.set_color(green)
        else:
            self.low_value_text.set_color(white)

        percentage = round(((data['Close'] - prev_price) * 100) / prev_price, 2)
        if change > 0:
            self.change_value_text.set_color(red)
            self.close_value_text.set_color(red)
            self.volume_value_text.set_color(red)
        elif change < 0:
            self.change_value_text.set_color(green)
            self.close_value_text.set_color(green)
            self.volume_value_text.set_color(green)
        else:
            self.change_value_text.set_color(white)
            self.close_value_text.set_color(white)
            self.volume_value_text.set_color(white)

        self.date_text.set_text("日期: {date}".format(date=date_str))
        self.open_value_text.set_text("{open}".format(open=data['Open']))
        self.high_value_text.set_text("{high}".format(high=data['High']))
        self.low_value_text.set_text("{low}".format(low=data['Low']))
        self.close_value_text.set_text("{close}".format(close=data['Close']))
        self.change_value_text.set_text("{change}%".format(change=percentage))
        self.volume_value_text.set_text("{volume}".format(volume=int(data['Volume'])))

    def refresh_plot(self, idx_start: int, view_num: int):
        self.clear_axes()
        plot_data = self.data.iloc[idx_start:idx_start+view_num]

        params = {'type': 'candle', 'ax': self.main_ax, 'volume': self.volume_ax,
                  'datetime_format': '%y-%m-%d', 'xrotation': 0}
        # addplot
        if len(self.aps):
            aps = []
            for col, col_params in self.aps:
                aps.append(mpf.make_addplot(plot_data[col], **col_params))
            params['addplot'] = aps

        mpf.plot(data=plot_data, **params)
        # reset vertical line
        self.main_ax.set_ylabel('股價', fontproperties=MyFont, fontsize=8)
        self.main_ax_vertical_line = self.main_ax.axvline(color='#d49424', linewidth=1, linestyle="-")
        self.main_ax_vertical_line.set_xdata(self.idx_start)

        self.volume_ax.set_ylabel('成交量', fontproperties=MyFont, fontsize=8)
        self.volume_ax_vertical_line = self.volume_ax.axvline(color='#d49424', linewidth=1, linestyle="-")
        self.volume_ax_vertical_line.set_xdata(self.idx_start)

        if self.extra_ax:
            self.extra_ax.set_ylabel(self.extra_ax_ylabel, fontproperties=MyFont, fontsize=8)
            self.extra_ax_vertical_line = self.extra_ax.axvline(color='#d49424', linewidth=1, linestyle="-")
            self.extra_ax_vertical_line.set_xdata(self.idx_start)

        self.canvas.draw()
        if not self.canvas_bind_event_flag:
            self.canvas_bind_event_flag = True
            self.canvas.mpl_connect('button_press_event', self.on_press)
            self.canvas.mpl_connect('scroll_event', self.on_scroll)
            self.canvas.mpl_connect('motion_notify_event', self.on_motion)
            self.canvas.mpl_connect('button_release_event', self.on_release)


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

        # set group layout
        group = QGroupBox("Params")
        group_layout = QGridLayout()
        group_layout.addWidget(code_label, 0, 0)
        group_layout.addWidget(code_combox, 0, 1)
        group_layout.addWidget(name_label, 0, 2)
        group_layout.addWidget(name_combox, 0, 3)
        group.setLayout(group_layout)
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        mpf_stock = QWidget()

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
        self.mpf_stock = mpf_stock

    @Slot()
    def execute_btn_fn(self):
        # add SMA data
        sma_df_names = ['MA5', 'MA10', 'MA20']
        sma_ap_params = [
            {'color': '#ffd700', 'width': 0.8},
            {'color': '#00ffff', 'width': 0.8},
            {'color': '#8a2be2',  'width': 0.8}]
        _ma5 = compute.sma(MyData['Close'].tolist(), n=5)
        _ma10 = compute.sma(MyData['Close'].tolist(), n=10)
        _ma20 = compute.sma(MyData['Close'].tolist(), n=20)
        main_data = pd.DataFrame(data={sma_df_names[0]: _ma5, sma_df_names[1]: _ma10, sma_df_names[2]: _ma20})
        data = MyData.join(main_data)

        # add MACD data
        macd_df_names = ['Signal', 'MACD', 'Diff']
        macd_ap_params = [
            {'color': '#ffd700', 'width': 0.8},
            {'color': '#00ffff', 'width': 0.8},
            {'color': 'dimgray', 'type': 'bar', 'alpha': 1}]
        _signal, _macd, _diff = compute.macd(MyData['Close'].tolist())
        extra_data = pd.DataFrame(
            data={macd_df_names[0]: _signal, macd_df_names[1]: _macd, macd_df_names[2]: _diff})
        data = data.join(extra_data)

        # set DF index
        data['Date'] = pd.DatetimeIndex(data['Date'])
        data.set_index('Date', inplace=True)

        layout = self.layout()
        layout.removeWidget(self.mpf_stock)
        self.mpf_stock.deleteLater()
        self.mpf_stock = MpfStockWidget(data=data, enable_extra_ax=True)
        self.mpf_stock.set_main_ax_addplot(columns=sma_df_names, columns_params=sma_ap_params)
        self.mpf_stock.set_extra_ax_addplot(columns=macd_df_names, columns_params=macd_ap_params, ylabel='MACD')
        self.mpf_stock.refresh_plot(idx_start=data.shape[0] - 1 - self.mpf_stock.view_num,
                                    view_num=self.mpf_stock.view_num)
        layout.addWidget(self.mpf_stock, 3, 0, 1, 2)  # noqa


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setCentralWidget(MainWidget())
        self.setWindowTitle("Example08")
        self.resize(1024, 720)
