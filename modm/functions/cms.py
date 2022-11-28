from os import path
import PyPDF2
from PySide6.QtCore import QDir
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QTreeView,
    QFileSystemModel,
    QListView,
    QMessageBox,

)
class ui_cms(QWidget):

    def __init__(self):
        super(ui_cms, self).__init__()
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
        self.document_view = QWebEngineView()
        self.document_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.document_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        document_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'ressources','modm_logo.svg')
        self.document_view.setUrl(f"file://{document_path}")
        layout_document = QVBoxLayout()
        layout_document.addWidget(self.document_view)

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
        self.setLayout(layout_cms)


    def open_folder(self,index):
        self.file_path = self.model_folders.filePath(index)
        self.model_files.setRootPath(self.file_path)
        self.model_files.setFilter(QDir.Files)
        self.widget_list_files.setModel(self.model_files)
        self.widget_list_files.setRootIndex(self.model_files.index(self.file_path))

    def open_document(self,index):
        document_path = self.model_files.filePath(index)
        try:
            PyPDF2.PdfReader(open(document_path, "rb"))
        except FileNotFoundError:
            QMessageBox.critical(self, "Open document error", (f"File {document_path} \n does not exist."))
        except PyPDF2.errors.PyPdfError as pdferror:
            QMessageBox.critical(self, "Open document error", (f"File {document_path} \n is invalid! \n Error: {str(pdferror)}"))
        else:
            self.document_view.setUrl(f"file://{document_path}")

