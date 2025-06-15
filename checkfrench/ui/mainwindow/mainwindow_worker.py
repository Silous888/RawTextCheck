# -------------------- Import Lib Tier -------------------
from PyQt5.QtCore import QObject, pyqtSignal

# -------------------- Import Lib User -------------------
from checkfrench.script import process
from checkfrench.script import utils


class WorkerMainWindow(QObject):

    signal_get_name_sheet_start = pyqtSignal(str)
    signal_languagetool_initialize_start = pyqtSignal()
    signal_language_tool_process_start = pyqtSignal(str, str)

    signal_get_name_sheet_finished = pyqtSignal(object)
    signal_languagetool_initialize_finished = pyqtSignal()
    signal_language_tool_process_finished = pyqtSignal(object)
    signal_process_loop = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

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
