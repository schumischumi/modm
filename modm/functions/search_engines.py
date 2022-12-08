"""_summary_
"""
from os import path
import re
from subprocess import SubprocessError, run
from PySide6.QtWidgets import (
    QMessageBox,
)


class UiSearch():
    """This class extends

    """

    def __init__(self, selected_engine):
        super(UiSearch, self).__init__()
        # todo: move to settings or config

        self.engine_name = selected_engine
        self.engine_path = '/usr/bin/baloosearch'
        self.error_box = QMessageBox()
        self.validate_engine()
        if self.engine_name == "baloo":
            self.sanatize_whitelist = r"[^0-9a-zA-Z\/.,\s]+"
            self.allowed_characters = """
                - A-Z
                - a-z
                - 0-9
                - , . /
                - Space
                """
        elif self.engine_name == "elastic":
            self.sanatize_whitelist = r"[^0-9a-zA-Z\/.,\s]+"
            self.allowed_characters = """
                - A-Z
                - a-z
                - 0-9
                - , . /
                - Space
                """

    def validate_engine(self) -> bool:
        """validates if the the search engines works as expected

        Returns:
            bool: result of the validation
        """
        supported_engines = ['baloo', 'elastic']
        if self.engine_name not in supported_engines:
            QMessageBox.critical(self.error_box, "Search Engine Error",
                                 (f"Search Engine {self.engine_name} is not supported!"))
            return False
        if self.engine_name == "baloo":
            if not path.isfile(self.engine_path):
                QMessageBox.critical(self.error_box, "Search Engine Error",
                                     f"Binary {self.engine_path} for search "
                                     f"engine {self.engine_name} does not exist!")
                return False

            exec_version = run([self.engine_path, '--version'],
                               capture_output=True, text=True, check=True, shell=False)

            if exec_version.returncode:
                QMessageBox.critical(self.error_box, "Search Engine Error",
                                     f"Version Check for search engine {self.engine_name} "
                                     f"was not successful: {exec_version.stdout}")
                return False

        elif self.engine_name == "elastic":
            return False
        else:
            return False

        return True

    def search_by_name(self, query: str, directory: str, extension: str = ".pdf"):
        """_summary_

        Args:
            query (str): _description_
            directory (str): _description_
            type (str, optional): _description_. Defaults to "Document".
            extension (str, optional): _description_. Defaults to ".pdf".

        Returns:
            _type_: _description_
        """
        if self.engine_name == "baloo":
            clean_query = re.sub(self.sanatize_whitelist, "", query)
            search_results = self.baloo_search(
                query=clean_query, directory=directory, extension=extension)
        elif self.engine_name == "elastic":
            return None
        else:
            return None

        return search_results

    def baloo_search(self, query: str, directory: str,
                     doc_type: str = "Document", extension: str = ".pdf"):
        """_summary_
        Args:
            query (str): _description_
            directory (str, optional): _description_. Defaults to "".
            type (str, optional): _description_. Defaults to "Document".
            extension (str, optional): _description_. Defaults to ".pdf".

        Returns:
            _type_: _description_
        """
        search_results = []
        # validate doc_type
        try:
            exec_search = run([self.engine_path, query, extension,
                               "type:"+doc_type, '-d', directory],
                              capture_output=True, text=True, check=True, shell=False)
        except SubprocessError as sub_error:
            QMessageBox.critical(self.error_box, "Search Engine Error",
                                 f"Version Check for search engine {str(sub_error)} ")
        search_results = exec_search.stdout.split('\n')
        # search_results.pop(-1)
        return search_results
