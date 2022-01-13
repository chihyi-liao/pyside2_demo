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
