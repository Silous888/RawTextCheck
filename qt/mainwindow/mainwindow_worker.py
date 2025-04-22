# -------------------- Import Lib Tier -------------------
from PyQt5.QtCore import QObject, pyqtSignal

# -------------------- Import Lib User -------------------
from script import process
from script import utils


class WorkerMainWindow(QObject):

    signal_load_word_excluded_start = pyqtSignal(int)
    signal_get_name_sheet_start = pyqtSignal(str)
    signal_languagetool_initialize_start = pyqtSignal()
    signal_language_tool_process_start = pyqtSignal(str, str)
    signal_find_string_process_start = pyqtSignal(str, str, str)
    signal_replace_string_process_start = pyqtSignal(str, str, str, str, str, int)
    signal_add_specific_words_start = pyqtSignal()

    signal_load_word_excluded_finished = pyqtSignal()
    signal_get_name_sheet_finished = pyqtSignal(object)
    signal_languagetool_initialize_finished = pyqtSignal()
    signal_language_tool_process_finished = pyqtSignal(object)
    signal_find_string_process_finished = pyqtSignal(object)
    signal_replace_string_process_finished = pyqtSignal(int, str, str)
    signal_add_specific_words_finished = pyqtSignal()
    signal_process_loop = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    def load_excluded_word_in_table_thread(self, sheet_index: int) -> None:
        process.get_list_specific_word(sheet_index)
        self.signal_load_word_excluded_finished.emit()

    def get_name_sheet_thread(self, url: str) -> None:
        result: tuple[str, str] | int = process.get_name_and_type_of_url(url)
        self.signal_get_name_sheet_finished.emit(result)

    def languagetool_initialize_thread(self) -> None:
        process.language_tool_initialize()
        self.signal_languagetool_initialize_finished.emit()

    def language_tool_process_thread(self, url: str, column_letter: str) -> None:
        output: list[tuple[int, str, str]] | int = process.language_tool_process(url, column_letter)
        if isinstance(output, int):
            return
        output_name: list[tuple[str, int, str]] = process.add_filename_to_output2(url, output)  # type: ignore
        name_file: str | int = process.gdrive.get_name_by_id(utils.extract_google_drive_id(url))
        if isinstance(name_file, int):
            name_file = ""
        self.signal_language_tool_process_finished.emit((output_name, name_file))
        self.signal_process_loop.emit()

    def find_string_process_thread(self, url: str, column_letter: str, string_to_search: str) -> None:
        output: list[tuple[int, str]] | int = process.search_string_in_sheet(url, column_letter, string_to_search)
        if isinstance(output, int):
            return
        output_name: list[tuple[str, int, str]] = process.add_filename_to_output(url, output)  # type: ignore
        name_file: str | int = process.gdrive.get_name_by_id(utils.extract_google_drive_id(url))
        if isinstance(name_file, int):
            name_file = ""
        self.signal_find_string_process_finished.emit((output_name, name_file))
        self.signal_process_loop.emit()

    def replace_string_process_thread(self, filename: str, column_letter: str, line: str,
                                      old_text: str, new_text: str, index: int) -> None:
        process.replace_text_in_cell(filename, column_letter, line, old_text, new_text)
        self.signal_replace_string_process_finished.emit(index, old_text, new_text)

    def add_specific_words_thread(self) -> None:
        process.add_list_specific_word()
        self.signal_add_specific_words_finished.emit()
