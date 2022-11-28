import sys
from PySide6.QtGui import QPalette, QColor,QScreen
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
)
from modm.functions.cms import ui_cms

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My Own Document Management")
        screen_size = QScreen.availableGeometry(QApplication.primaryScreen())

        #Get Screen Width
        screen_size_x=screen_size.width()

        #Get Screen Height
        screen_size_y=screen_size.height()

        #Pyside Window State maximized
        self.setGeometry(0, 0, screen_size_x, screen_size_y)

        self.file_path = '/home/user/Downloads'


        # Tab Menu
        tab_menu = QTabWidget()
        tab_menu.setTabPosition(QTabWidget.West)
        tab_menu.setMovable(True)
        tab_menu.addTab(ui_cms(), 'CMS')
        tab_menu.addTab(Color('red'), 'Merge')
        tab_menu.addTab(Color('red'), 'Split')
        tab_menu.addTab(Color('red'), 'Rename')
        tab_menu.addTab(Color('red'), 'Edit')
        tab_menu.addTab(Color('red'), 'Scan')
        tab_menu.addTab(Color('red'), 'Settings')
        tab_menu.addTab(Color('red'), 'Help')
        self.setCentralWidget(tab_menu)


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()

if __name__ == '__main__':
    run()
