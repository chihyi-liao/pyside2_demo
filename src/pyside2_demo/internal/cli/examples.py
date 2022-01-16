import sys
import click

from PySide2.QtWidgets import QApplication


@click.group(name="example", help="GUI 範例程式")
def example_group():
    pass


@example_group.command(name="01", help="Login範例")
def example_01():
    from pyside2_demo.internal.views.examples.example01 import MainWindow, LoginDialog
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_():
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())


@example_group.command(name="02", help="Layout範例")
def example_02():
    from pyside2_demo.internal.views.examples.example02 import MainWindow
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


@example_group.command(name="03", help="QListWidget範例")
def example_03():
    from pyside2_demo.internal.views.examples.example03 import MainWindow
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


@example_group.command(name="04", help="QTableWidget範例")
def example_04():
    from pyside2_demo.internal.views.examples.example04 import MainWindow
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
