"""functions of the UI"""

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QCloseEvent

# -------------------- Import Lib User -------------------
from qt_files.Ui_mainwindow import Ui_MainWindow
from windows_logic.dialog_excluded_words import DialogExcludedWords
import process


# -------------------------------------------------------------------#
#                          CLASS WORKER                              #
# -------------------------------------------------------------------#
class _WorkerMainWindow(QObject):

    signal_load_word_excluded_start = pyqtSignal(int)
    signal_has_access_to_element_start = pyqtSignal(str)
    signal_orthocheck_load_dictionary_start = pyqtSignal()

    signal_load_word_excluded_finished = pyqtSignal()
    signal_has_access_to_element_finished = pyqtSignal(bool)
    signal_orthocheck_load_dictionary_finished = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    def load_excluded_word_in_table_thread(self, sheet_index: int) -> None:
        process.get_list_specific_word(sheet_index)
        self.signal_load_word_excluded_finished.emit()

    def has_access_to_element_thread(self, url: str) -> None:
        result: bool = process.has_access_to_element(url)
        self.signal_has_access_to_element_finished.emit(result)

    def orthocheck_load_dictionary_thread(self) -> None:
        process.orthocheck_load_dictionary()
        self.signal_orthocheck_load_dictionary_finished.emit()


# -------------------------------------------------------------------#
#                         CLASS MAINWINDOW                           #
# -------------------------------------------------------------------#
class MainWindow(QMainWindow):
    """main window of the application

    Args:
        QMainWindow (QMainWindow): main window of the application
    """
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore

        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = _WorkerMainWindow()
        self.m_worker.moveToThread(self.m_thread)

        self.is_url_correct: bool = False
        self.is_orthocheck_available: bool = False
        self.ui.pushButton_method_1.setEnabled(False)

        self.urlsheet_timer = QTimer(self)
        self.urlsheet_timer.setSingleShot(True)
        self.urlsheet_timer.setInterval(1000)  # 1 seconde

        self.populate_combobox_game()
        self.toggle_ui_enabled_except_combobox_game(False)
        self.set_up_connect()

        self.m_worker.signal_orthocheck_load_dictionary_start.emit()

    def populate_combobox_game(self) -> None:
        """populate comboBox_game
        """
        self.ui.comboBox_game.addItem("-- Choisissez un jeu --")
        for game in process.data_json:
            self.ui.comboBox_game.addItem(game["title"])  # type: ignore

    def toggle_ui_enabled_except_combobox_game(self, enabled: bool) -> None:
        """toggle the enabled state of the ui except the comboBox_game

        Args:
            enabled (bool): enabled state
        """
        self.ui.pushButton_gameDictionary.setEnabled(enabled)
        self.toggle_ui_enabled_buttons_methods(enabled)
        self.ui.lineEdit_urlSheet.setEnabled(enabled)
        self.ui.lineEdit_frenchColumn.setEnabled(enabled)
        if not enabled or self.is_url_correct:
            self.ui.tabWidget_result.setEnabled(enabled)

    def toggle_ui_enabled_buttons_methods(self, enabled: bool) -> None:
        """toggle the enabled state of the buttons of check methods

        Args:
            enabled (bool): enabled state
        """
        if not enabled or (self.is_orthocheck_available and self.is_url_correct):
            self.ui.pushButton_method_1.setEnabled(enabled)
        if not enabled or self.is_url_correct:
            self.ui.pushButton_method_2.setEnabled(enabled)
        if not enabled or self.is_url_correct:
            self.ui.pushButton_method_3.setEnabled(enabled)

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        # pushButton
        self.ui.pushButton_gameDictionary.clicked.connect(self.pushbutton_gamedictionary_clicked)
        self.ui.pushButton_method_1.clicked.connect(self.pushbutton_method_1_clicked)
        self.ui.pushButton_method_2.clicked.connect(self.pushbutton_method_2_clicked)
        self.ui.pushButton_method_3.clicked.connect(self.pushbutton_method_3_clicked)
        # lineEdit
        self.ui.lineEdit_urlSheet.textChanged.connect(self.lineedit_urlsheet_textchanged)
        self.urlsheet_timer.timeout.connect(self.check_urlsheet_access)
        self.ui.lineEdit_frenchColumn.textChanged.connect(self.lineedit_frenchcolumn_textchanged)
        # comboBox
        self.ui.comboBox_game.currentIndexChanged.connect(self.combobox_game_currentindexchanged)
        # thread start
        self.m_worker.signal_load_word_excluded_start.connect(
            self.m_worker.load_excluded_word_in_table_thread)
        self.m_worker.signal_has_access_to_element_start.connect(
            self.m_worker.has_access_to_element_thread)
        self.m_worker.signal_orthocheck_load_dictionary_start.connect(
            self.m_worker.orthocheck_load_dictionary_thread
        )
        # thread finish
        self.m_worker.signal_load_word_excluded_finished.connect(self.load_dialog_finished)
        self.m_worker.signal_has_access_to_element_finished.connect(self.has_access_to_element_finished)
        self.m_worker.signal_orthocheck_load_dictionary_finished.connect(self.orthocheck_load_dictionary_finished)

    def pushbutton_gamedictionary_clicked(self) -> None:
        """slot for pushButton_gameDictionary
        """
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.ui.pushButton_gameDictionary.setEnabled(False)
        self.m_worker.signal_load_word_excluded_start.emit(self.ui.comboBox_game.currentIndex()-1)

    def pushbutton_method_1_clicked(self) -> None:
        """slot for pushButton_method_1
        """

    def pushbutton_method_2_clicked(self) -> None:
        """slot for pushButton_method_2
        """

    def pushbutton_method_3_clicked(self) -> None:
        """slot for pushButton_method_3
        """

    def lineedit_urlsheet_textchanged(self) -> None:
        """slot for lineEdit_urlSheet
        """
        text: str = self.ui.lineEdit_urlSheet.text()
        if len(text) < 1:
            self.ui.lineEdit_urlSheet.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.is_url_correct = False
        else:
            self.urlsheet_timer.start()

    def check_urlsheet_access(self) -> None:
        """Vérifier l'accès à l'élément après un délai"""
        text: str = self.ui.lineEdit_urlSheet.text()
        self.m_worker.signal_has_access_to_element_start.emit(text)

    def lineedit_frenchcolumn_textchanged(self, text: str) -> None:
        """slot for lineEdit_frenchColumn
        """

    def combobox_game_currentindexchanged(self, index: int) -> None:
        """slot for comboBox_game
        """
        self.toggle_ui_enabled_except_combobox_game(bool(index))
        self.ui.lineEdit_frenchColumn.setText(process.data_json[index - 1]["column_sheet"])  # type: ignore

    def load_dialog_finished(self) -> None:
        """slot for signal load_dialog_finished
        """
        QApplication.restoreOverrideCursor()
        self.dialog_dict = DialogExcludedWords()
        self.dialog_dict.load_excluded_word_in_table()
        self.dialog_dict.exec()
        self.ui.pushButton_gameDictionary.setEnabled(True)

    def has_access_to_element_finished(self, result: bool) -> None:
        self.is_url_correct = result
        if self.is_url_correct:
            self.ui.lineEdit_urlSheet.setStyleSheet("background-color: rgb(0, 200, 0);")
            self.toggle_ui_enabled_buttons_methods(True)
        else:
            self.ui.lineEdit_urlSheet.setStyleSheet("background-color: rgb(200, 0, 0);")
            self.toggle_ui_enabled_buttons_methods(False)

    def orthocheck_load_dictionary_finished(self) -> None:
        self.is_orthocheck_available = True
        self.ui.pushButton_method_1.setEnabled(bool(self.ui.comboBox_game.currentIndex()))

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.m_thread.isRunning():
            self.m_thread.quit()
            self.m_thread.wait()
        a0.accept()
