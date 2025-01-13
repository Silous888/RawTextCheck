"""functions of the UI"""

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal, pyqtSlot

# -------------------- Import Lib User -------------------
from qt_files.Ui_mainwindow import Ui_MainWindow
from windows_logic.dialog_excluded_words import DialogExcludedWords
import process


# -------------------------------------------------------------------#
#                          CLASS WORKER                              #
# -------------------------------------------------------------------#
class _Worker(QObject):

    signal_load_word_excluded_start = pyqtSignal(int)
    signal_load_word_excluded_finished = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    @pyqtSlot(int)
    def load_excluded_word_in_table_thread(self, sheet_index: int) -> None:
        process.get_list_specific_word(sheet_index)
        self.signal_load_word_excluded_finished.emit()


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
        self.m_worker = _Worker()
        self.m_worker.moveToThread(self.m_thread)

        self.populate_combobox_game()
        self.toggle_ui_enabled_except_combobox_game(False)
        self.set_up_connect()

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
        self.ui.pushButton_method_1.setEnabled(enabled)
        self.ui.pushButton_method_2.setEnabled(enabled)
        self.ui.pushButton_method_3.setEnabled(enabled)
        self.ui.lineEdit_urlSheet.setEnabled(enabled)
        self.ui.lineEdit_frenchColumn.setEnabled(enabled)
        self.ui.tabWidget_result.setEnabled(enabled)

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        # pushButton
        self.ui.pushButton_gameDictionary.clicked.connect(self.pushbutton_gamedictionary_clicked)
        self.ui.pushButton_method_1.clicked.connect(self.pushbutton_method_1_clicked)
        self.ui.pushButton_method_2.clicked.connect(self.pushbutton_method_2_clicked)
        self.ui.pushButton_method_3.clicked.connect(self.pushbutton_method_3_clicked)
        # lineEdit
        self.ui.lineEdit_urlSheet.editingFinished.connect(self.lineedit_urlsheet_textchanged)
        self.ui.lineEdit_frenchColumn.textChanged.connect(self.lineedit_frenchcolumn_textchanged)
        # comboBox
        self.ui.comboBox_game.currentIndexChanged.connect(self.combobox_game_currentindexchanged)
        # thread
        self.m_worker.signal_load_word_excluded_start.connect(self.m_worker.load_excluded_word_in_table_thread)
        self.m_worker.signal_load_word_excluded_finished.connect(self.load_dialog_finished)

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
            print(text)
            self.ui.lineEdit_urlSheet.setStyleSheet("background-color: rgb(255, 255, 255);")
        elif process.has_access_to_element(text):
            self.ui.lineEdit_urlSheet.setStyleSheet("background-color: rgb(0, 200, 0);")
        else:
            self.ui.lineEdit_urlSheet.setStyleSheet("background-color: rgb(200, 0, 0);")

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
