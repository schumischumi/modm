import sys
from PySide6.QtCore import QDir

from PySide6.QtGui import QPalette, QColor,QScreen
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QTreeView,
    QFileSystemModel,
    QListView
)
from modm.functions.cms import cms

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

        layout_cms = QHBoxLayout()

        # Folder Layout
        self.widget_tree_folders = QTreeView()
        self.widget_tree_folders.clicked.connect(self.open_folder)
        self.model_folders = QFileSystemModel()
        self.model_folders.setFilter(QDir.NoDotDot | QDir.Dirs)
        layout_cms.addWidget(self.widget_tree_folders,stretch=1)

        # Files Layout
        layout_files = QVBoxLayout()

        layout_files_search = QHBoxLayout()

        search_input_text = QLineEdit()
        search_input_text.setMaxLength(10)
        search_input_text.setPlaceholderText("Enter your text")
        layout_files_search.addWidget(search_input_text)

        search_button_search = QPushButton("Search")
        layout_files_search.addWidget(search_button_search)

        self.widget_list_files = QListView()
        self.widget_list_files.clicked.connect(self.open_document)
        self.model_files = QFileSystemModel()
        self.model_files.setNameFilterDisables(False)
        self.model_files.setFilter(QDir.Files)
        self.model_files.setNameFilters(["*.pdf"])

        layout_files.addLayout(layout_files_search)
        layout_files.addWidget(self.widget_list_files)

        layout_cms.addLayout( layout_files,stretch=2)

        # Document Layout
        self.view = QWebEngineView()
        self.view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        layout_document = QVBoxLayout()
        layout_document.addWidget(self.view)

        # Document Layout -> buttons
        layout_document_buttons = QHBoxLayout()
        document_button_merge = QPushButton("Merge")
        layout_document_buttons.addWidget(document_button_merge)
        document_button_split = QPushButton("Split")
        layout_document_buttons.addWidget(document_button_split)
        document_button_edit = QPushButton("Edit")
        layout_document_buttons.addWidget(document_button_edit)
        document_button_print = QPushButton("Print")
        layout_document_buttons.addWidget(document_button_print)
        document_button_share = QPushButton("Share")
        layout_document_buttons.addWidget(document_button_share)
        document_button_mail = QPushButton("Mail")
        layout_document_buttons.addWidget(document_button_mail)

        layout_document.addLayout(layout_document_buttons)
        layout_cms.addLayout(layout_document,stretch=3)

        self.model_folders.setRootPath(self.file_path)
        self.widget_tree_folders.setModel(self.model_folders)
        self.widget_tree_folders.setRootIndex(self.model_folders.index(self.file_path))

        self.model_files.setRootPath(self.file_path)
        self.widget_list_files.setModel(self.model_files)
        self.widget_list_files.setRootIndex(self.model_files.index(self.file_path))
        self.widget_cms = QWidget()
        self.widget_cms.setLayout(layout_cms)

        content_cms = cms()
        # Tab Menu
        tab_menu = QTabWidget()
        tab_menu.setTabPosition(QTabWidget.West)
        tab_menu.setMovable(True)
        tab_menu.addTab(content_cms.widget_cms, 'CMS')
        tab_menu.addTab(self.widget_cms, 'Merge')
        tab_menu.addTab(Color('red'), 'Split')
        tab_menu.addTab(Color('red'), 'Rename')
        tab_menu.addTab(Color('red'), 'Edit')
        tab_menu.addTab(Color('red'), 'Scan')
        tab_menu.addTab(Color('red'), 'Settings')
        tab_menu.addTab(Color('red'), 'Help')
        self.setCentralWidget(tab_menu)

    def open_folder(self,index):
        self.file_path = self.model_folders.filePath(index)
        self.model_files.setRootPath(self.file_path)
        self.model_files.setFilter(QDir.Files)
        self.widget_list_files.setModel(self.model_files)
        self.widget_list_files.setRootIndex(self.model_files.index(self.file_path))

    def open_document(self,index):
        self.view.setUrl(f"file://{self.model_files.filePath(index)}")
def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()

if __name__ == '__main__':
    run()
