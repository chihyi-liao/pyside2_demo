import hashlib
import sys
import traceback

from PySide2.QtCore import QObject, QRunnable, Signal, Slot, Qt
from PySide2.QtGui import QPainter, QPen, QColor, QPixmap, QPainterPath
from PySide2.QtWidgets import QLabel, QFrame


def draw_sketch(painter: QPainter, x: int, y: int, width: int, height: int, color: QColor = Qt.red, brush: int = 1):
    painter.setPen(QPen(color, brush, Qt.SolidLine))
    painter.drawRect(x, y, width, height)


def hash_password(password: str) -> str:
    """ 雜湊明文密碼 """
    m = hashlib.sha1()
    m.update(password.encode("utf-8"))
    return m.hexdigest()


def is_valid_user(name, password):
    """ 驗證帳號密碼(虛擬) """
    fake_users_db = {"admin": {"username": "admin", "password": hash_password("password")}}
    user = fake_users_db.get(name)
    if user:
        if user['password'] == hash_password(password):
            return True
    return False


class WorkerSignals(QObject):
    """ Defines the signals available from a running worker thread.

    Supported signals are:
    finished: No data
    cancel: No data
    error: `tuple` (exctype, value, traceback.format_exc() )
    result: `object` data returned from processing, anything
    progress: `int` indicating % progress
    """
    finished = Signal()
    cancel = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(tuple)


class Worker(QRunnable):
    """ Worker thread """

    def __init__(self, fn, *args, **kwargs):
        """Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
           :param fn: The function callback to run on this worker thread. Supplied args and
                       kwargs will be passed through to the runner.
           :param args: Arguments to pass to the callback function
           :param kwargs: Keywords to pass to the callback function
        """
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        """ Initialise the runner function with passed args, kwargs. """
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:  # noqa
            traceback.print_exc()
            exc_type, value = sys.exc_info()[:2]
            self.signals.error.emit((exc_type, value, traceback.format_exc()))  # noqa
        else:
            self.signals.result.emit(result)  # noqa
        finally:
            self.signals.finished.emit()  # noqa


class RoundAvatar(QLabel):
    def __init__(self, *args, antialiasing=True, filepath="", avatar_size=50, **kwargs):
        """ 產生圓形的頭像 """
        super(RoundAvatar, self).__init__(*args, **kwargs)
        self.Antialiasing = antialiasing
        self.setMaximumSize(avatar_size, avatar_size)
        self.setMinimumSize(avatar_size, avatar_size)
        self.radius = int(avatar_size / 2)
        self.target = QPixmap(self.size())
        self.target.fill(Qt.transparent)

        p = QPixmap(filepath).scaled(
            avatar_size, avatar_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        if self.Antialiasing:
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(
            0, 0, self.width(), self.height(), self.radius, self.radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
