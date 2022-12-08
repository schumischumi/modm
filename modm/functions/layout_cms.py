"""_summary_
"""
import re
from os import path
import PyPDF2
from PySide6.QtCore import QDir, QModelIndex, QDirIterator, Qt
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
    QStyle,
    QTableView,
    QHeaderView

)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from modm.functions.search_engines import UiSearch


class UiCms(QWidget):
    """This class extends

    Args:
        QWidget (class): PySide6.QtWidgets class
    """

    def __init__(self):
        super(UiCms, self).__init__()
        self.file_path = '/home/user/Downloads'

        layout_cms = QHBoxLayout()

        # Folder Layout
        self.widget_tree_folders = QTreeView()
        self.widget_tree_folders.clicked.connect(self.open_folder)
        self.model_folders = QFileSystemModel()
        self.model_folders.setFilter(QDir.NoDotDot | QDir.Dirs)
        layout_cms.addWidget(self.widget_tree_folders, stretch=1)

        # Files Layout
        layout_files = QVBoxLayout()

        layout_files_search = QHBoxLayout()

        self.search_input_text = QLineEdit()
        self.search_input_text.setMaxLength(100)
        self.search_input_text.setPlaceholderText("Enter your text")
        self.search_input_text.textChanged.connect(
            self.update_search_information)
        self.search_input_text.editingFinished.connect(self.search_document)
        layout_files_search.addWidget(self.search_input_text)
        # SP_MessageBoxWarning
        self.search_button_sanatize = QPushButton()
        button_sanatize_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_MessageBoxInformation)
        self.search_button_sanatize.setIcon(button_sanatize_icon)
        self.search_button_sanatize.setCheckable(True)
        self.bad_charaters = False
        self.search_button_sanatize.clicked.connect(self.show_sanatize_message)
        layout_files_search.addWidget(self.search_button_sanatize)

        search_button_search = QPushButton("Search")
        search_button_search.setCheckable(True)
        search_button_search.clicked.connect(self.search_document)
        layout_files_search.addWidget(search_button_search)

        # self.widget_list_files = QListView()
        self.widget_list_files = QTableView()
        self.widget_list_files.clicked.connect(self.open_document)
        self.model_files = QStandardItemModel()
        self.model_files.setColumnCount(3)
        self.widget_list_files.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)
        self.widget_list_files.horizontalHeader().setStretchLastSection(True)
        self.widget_list_files.verticalHeader().hide()

        layout_files.addLayout(layout_files_search)
        layout_files.addWidget(self.widget_list_files)

        layout_cms.addLayout(layout_files, stretch=2)

        # Document Layout
        self.document_view = QWebEngineView()
        self.document_view.settings().setAttribute(
            QWebEngineSettings.PluginsEnabled, True)
        self.document_view.settings().setAttribute(
            QWebEngineSettings.PdfViewerEnabled, True)
        document_path = path.join(path.dirname(path.dirname(
            path.abspath(__file__))), 'ressources', 'modm_logo.svg')
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
        layout_cms.addLayout(layout_document, stretch=3)

        self.model_folders.setRootPath(self.file_path)
        self.widget_tree_folders.setModel(self.model_folders)
        self.widget_tree_folders.setRootIndex(
            self.model_folders.index(self.file_path))
        self.widget_tree_folders.hideColumn(1)
        self.widget_tree_folders.hideColumn(2)
        self.widget_tree_folders.hideColumn(3)
        self.widget_list_files.setModel(self.model_files)
        self.open_folder(index=None)
        self.setLayout(layout_cms)
        self.search_instance = UiSearch(selected_engine='baloo')

    def open_folder(self, index: QModelIndex = None) -> None:
        """passes the path of the selected folder into the files QListView

        Args:
            index (PySide6.QtCore.QModelIndex): Index of the selected folder
        """
        if index is not None:
            self.file_path = self.model_folders.filePath(index)
        self.model_files.clear()
        iterator_items = QDirIterator(self.file_path, ["*.pdf"], QDir.Files)
        while iterator_items.hasNext():
            iterator_items.next()
            item_name = QStandardItem(iterator_items.fileName())
            item_dir = QStandardItem(path.dirname(iterator_items.filePath()))
            item_path = QStandardItem(iterator_items.filePath())
            self.model_files.appendRow([item_name, item_dir, item_path])
        self.model_files.setHorizontalHeaderLabels(
            ['Name', 'Directory', 'Path'])
        self.widget_list_files.setModel(self.model_files)
        self.widget_list_files.setColumnHidden(2, True)

    def open_document(self, index: QModelIndex) -> None:
        """loads the path of the selected file into the webview
        Args:
            index (PySide6.QtCore.QModelIndex): Index of the selected file
        """
        document_path = self.model_files.item(index.row(), 2).text()
        try:
            PyPDF2.PdfReader(open(document_path, "rb"))
        except FileNotFoundError:
            QMessageBox.critical(self, "Open document error",
                                 (f"File {document_path} \n does not exist."))
        except PyPDF2.errors.PyPdfError as pdferror:
            QMessageBox.critical(self, "Open document error", (
                f"File {document_path} \n is invalid! \n Error: {str(pdferror)}"))
        else:
            self.document_view.setUrl(f"file://{document_path}")

    def search_document(self):
        """_summary_
        """
        if self.search_input_text.text() is None or self.search_input_text.text() == "":
            QMessageBox.warning(self, "Search document warning",
                                "Please enter a string to search")
            return None
        # maybe move to init
        #search_instance = UiSearch(selected_engine='baloo')
        document_list = self.search_instance.search_by_name(
            query=self.search_input_text.text(), directory=self.file_path)
        self.model_files.clear()
        for item in document_list:
            item_name = QStandardItem(path.basename(item))
            item_dir = QStandardItem(path.dirname(item))
            item_path = QStandardItem(item)
            self.model_files.appendRow([item_name, item_dir, item_path])
        self.model_files.setHorizontalHeaderLabels(
            ['Name', 'Directory', 'Path'])
        self.widget_list_files.setModel(self.model_files)
        self.widget_list_files.setColumnHidden(2, True)

    def update_search_information(self, text):
        """_summary_
        """
        # if self.search_input_text.text() is not None and self.search_input_text.text() != "":
        if text is not None:
            if re.search(self.search_instance.sanatize_whitelist, text):
                self.bad_charaters = True
                button_sanatize_icon = self.style().standardIcon(
                    QStyle.StandardPixmap.SP_MessageBoxWarning)
            else:
                self.bad_charaters = False
                button_sanatize_icon = self.style().standardIcon(
                    QStyle.StandardPixmap.SP_MessageBoxInformation)
            self.search_button_sanatize.setIcon(button_sanatize_icon)

    def show_sanatize_message(self):
        """_summary_
        """
        if self.bad_charaters:
            QMessageBox.warning(self, "Search Warning",
                                "You use forbidden characters in your search query. \n"
                                "Only the followning characters are allowed and everything "
                                "else will be ignored:\n" + self.search_instance.allowed_characters)
        else:
            QMessageBox.information(self, "Search Information",
                                    "Only the followning characters are allowed and everything "
                                    "else will be ignored:\n" + self.search_instance.allowed_characters)
