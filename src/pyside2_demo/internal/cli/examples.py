import sys
import click

from PySide2.QtWidgets import QApplication, QStyleFactory


@click.group(name="example", help="GUI 範例程式")
def example_group():
    pass


@example_group.command(name="01", help="Login範例")
@click.option('--style', '-s', type=click.Choice(QStyleFactory.keys()),
              default=QStyleFactory.keys()[0], show_default=True, help='介面風格')
def example_01(style: str):
    from pyside2_demo.internal.views.examples.example01 import MainWindow, LoginDialog
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create(style))
    login = LoginDialog()
    if login.exec_():
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())


@example_group.command(name="02", help="Layout範例")
@click.option('--style', '-s', type=click.Choice(QStyleFactory.keys()),
              default=QStyleFactory.keys()[0], show_default=True, help='介面風格')
def example_02(style: str):
    from pyside2_demo.internal.views.examples.example02 import MainWindow
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create(style))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


@example_group.command(name="03", help="QListWidget範例")
@click.option('--style', '-s', type=click.Choice(QStyleFactory.keys()),
              default=QStyleFactory.keys()[0], show_default=True, help='介面風格')
def example_03(style: str):
    from pyside2_demo.internal.views.examples.example03 import MainWindow
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create(style))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


@example_group.command(name="04", help="QTableWidget範例")
@click.option('--style', '-s', type=click.Choice(QStyleFactory.keys()),
              default=QStyleFactory.keys()[0], show_default=True, help='介面風格')
def example_04(style: str):
    from pyside2_demo.internal.views.examples.example04 import MainWindow
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create(style))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


@example_group.command(name="05", help="QTabWidget範例")
@click.option('--style', '-s', type=click.Choice(QStyleFactory.keys()),
              default=QStyleFactory.keys()[0], show_default=True, help='介面風格')
def example_05(style: str):
    from pyside2_demo.internal.views.examples.example05 import MainWindow
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create(style))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


@example_group.command(name="06", help="QT Matplotlib範例")
@click.option('--style', '-s', type=click.Choice(QStyleFactory.keys()),
              default=QStyleFactory.keys()[0], show_default=True, help='介面風格')
def example_06(style: str):
    from pyside2_demo.internal.views.examples.example06 import MainWindow
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create(style))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
