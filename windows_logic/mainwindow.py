"""functions of the UI"""

from typing import Union, Sequence, Any
# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMenu, QAction, QTableWidget
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal, QTimer, QPoint
from PyQt5.QtGui import QCloseEvent

# -------------------- Import Lib User -------------------
from qt_files.Ui_mainwindow import Ui_MainWindow
from windows_logic.dialog_excluded_words import DialogExcludedWords
from windows_logic.confirm_exit import ConfirmExit
import process
import json_management as json_man


# -------------------------------------------------------------------#
#                          CLASS WORKER                              #
# -------------------------------------------------------------------#
class _WorkerMainWindow(QObject):

    signal_load_word_excluded_start = pyqtSignal(int)
    signal_get_name_sheet_start = pyqtSignal(str)
    signal_orthocheck_load_dictionary_start = pyqtSignal()
    signal_languagetool_initialize_start = pyqtSignal()
    signal_orthocheck_process_start = pyqtSignal(str, str)
    signal_language_tool_process_start = pyqtSignal(str, str)
    signal_word_check_process_start = pyqtSignal(str, str)
    signal_add_specific_words_start = pyqtSignal()

    signal_load_word_excluded_finished = pyqtSignal()
    signal_get_name_sheet_finished = pyqtSignal(object)
    signal_orthocheck_load_dictionary_finished = pyqtSignal()
    signal_languagetool_initialize_finished = pyqtSignal()
    signal_orthocheck_process_finished = pyqtSignal(object)
    signal_language_tool_process_finished = pyqtSignal(object)
    signal_word_check_process_finished = pyqtSignal(object)
    signal_add_specific_words_finished = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    def load_excluded_word_in_table_thread(self, sheet_index: int) -> None:
        process.get_list_specific_word(sheet_index)
        self.signal_load_word_excluded_finished.emit()

    def get_name_sheet_thread(self, url: str) -> None:
        result: str | int = process.get_name_sheet(url)
        self.signal_get_name_sheet_finished.emit(result)

    def orthocheck_load_dictionary_thread(self) -> None:
        process.orthocheck_load_dictionary()
        self.signal_orthocheck_load_dictionary_finished.emit()

    def languagetool_initialize_thread(self) -> None:
        process.language_tool_initialize()
        self.signal_languagetool_initialize_finished.emit()

    def orthocheck_process_thread(self, url: str, column_letter: str) -> None:
        output: list[tuple[int, str]] | int = process.orthocheck_process(url, column_letter)
        self.signal_orthocheck_process_finished.emit(output)

    def language_tool_process_thread(self, url: str, column_letter: str) -> None:
        output: list[tuple[int, str, str]] | int = process.language_tool_process(url, column_letter)
        self.signal_language_tool_process_finished.emit(output)

    def word_check_process_thread(self, url: str, column_letter: str) -> None:
        output: list[tuple[int, str]] | int = process.word_check_process(url, column_letter)
        self.signal_word_check_process_finished.emit(output)

    def add_specific_words_thread(self) -> None:
        process.add_list_specific_word()
        self.signal_add_specific_words_finished.emit()


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
        self.is_languagetool_available: bool = False
        self.ui.pushButton_method_1.setEnabled(False)
        self.ui.pushButton_uploadSpecificWords.setEnabled(False)

        self.ui.label_sheetOpened.setText("")
        self.ui.label_lastUdate_1.setText("")
        self.ui.label_lastUdate_2.setText("")
        self.ui.label_lastUdate_3.setText("")

        self.ui.tableWidget_3.setHidden(True)
        self.ui.tabWidget_result.removeTab(2)
        self.ui.pushButton_method_3.setHidden(True)
        self.ui.label_lastUdate_3.setHidden(True)

        self.urlsheet_timer = QTimer(self)
        self.urlsheet_timer.setSingleShot(True)
        self.urlsheet_timer.setInterval(1000)

        self.populate_combobox_game()
        self.toggle_ui_enabled_except_combobox_game(False)
        self.set_up_connect()

        self.ui.tabWidget_result

    def populate_combobox_game(self) -> None:
        """populate comboBox_game
        """
        self.ui.comboBox_game.addItem("-- Choisissez un jeu --")
        for game in json_man.data_json:
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
        self.toggle_ui_enabled_tabWidget_result(enabled)

    def toggle_ui_enabled_buttons_methods(self, enabled: bool) -> None:
        """toggle the enabled state of the buttons of check methods

        Args:
            enabled (bool): enabled state
        """
        if not enabled or self.is_url_correct:
            self.ui.pushButton_method_1.setEnabled(enabled)
        if not enabled or self.is_url_correct:
            self.ui.pushButton_method_2.setEnabled(enabled)
        if not enabled or self.is_url_correct:
            self.ui.pushButton_method_3.setEnabled(enabled)

    def toggle_ui_enabled_tabWidget_result(self, enabled: bool) -> None:
        """toggle the enabled state of the tabWidget_result

        Args:
            enabled (bool): enabled state
        """
        if not enabled or self.is_url_correct:
            self.ui.tabWidget_result.setEnabled(enabled)

    def add_to_specific_dictionary(self, item: QTableWidgetItem) -> None:
        """add to specific dictionary of the game

        Args:
            item (QTableWidgetItem): item from the table
        """
        process.list_specific_word_to_upload.append(item.text())
        self.remove_rows_table_by_text(self.ui.tableWidget_1, item.text())
        self.ui.pushButton_uploadSpecificWords.setText(
            str(len(process.list_specific_word_to_upload)) + " terme(s) à upload"
        )
        self.ui.pushButton_uploadSpecificWords.setEnabled(True)
        self.ui.comboBox_game.setEnabled(False)
        self.ui.pushButton_gameDictionary.setEnabled(False)
        textToolTip: str = "Veuillez uploader les termes avant de changer de jeu"
        self.ui.comboBox_game.setToolTip(textToolTip)
        self.ui.pushButton_gameDictionary.setToolTip(textToolTip)

    def add_to_global_dictionary(self, item: QTableWidgetItem) -> None:
        """add to global dictionary of the method

        Args:
            item (QTableWidgetItem): item from the table
        """
        process.orthocheck_add_word_to_csv(item.text())
        self.remove_rows_table_by_text(self.ui.tableWidget_1, item.text())

    def add_to_ignored_rules(self, item: QTableWidgetItem) -> None:
        """add to ignored rules of the game

        Args:
            item (QTableWidgetItem): item from the table
        """
        json_man.add_ignored_rules(process.id_current_game - 1,
                                   process.list_languagetool_current_file_rules[item.row()])

    def remove_rows_table_by_text(self, table: QTableWidget, text: str) -> None:
        rows_to_delete: list[int] = []
        for row in range(table.rowCount()):
            cell_item: QTableWidgetItem = table.item(row, 1)
            if cell_item and cell_item.text() == text:
                rows_to_delete.append(row)
        # Delete rows in reverse order to avoid messing up the row indices
        for row in reversed(rows_to_delete):
            table.removeRow(row)

    def delete_item(self, item: QTableWidgetItem) -> None:
        """Delete the selected item from the table.

        Args:
            item (QTableWidgetItem): item from the table
        """
        self.ui.tableWidget_1.removeRow(item.row())

    def delete_languagetool_item(self, item: QTableWidgetItem) -> None:
        """Delete the selected item from the table.

        Args:
            item (QTableWidgetItem): item from the table
        """

    def add_character(self, item: QTableWidgetItem) -> None:
        """Add the character to the authorized character for this game.

        Args:
            item (QTableWidgetItem): item from the table
        """
        json_man.add_correct_letter(process.id_current_game - 1, item.text()[0])
        json_man.load_json()
        self.remove_rows_table_by_text(self.ui.tableWidget_1, item.text())

    def add_punctuation(self, item: QTableWidgetItem) -> None:
        """Add the punctuation to the authorized punctuation for this game.

        Args:
            item (QTableWidgetItem): item from the table
        """
        json_man.add_correct_punctuation(process.id_current_game - 1, item.text()[0])
        json_man.load_json()
        self.remove_rows_table_by_text(self.ui.tableWidget_1, item.text())

    def update_table(
        self, table: QTableWidget, data: Sequence[Union[tuple[int, str], tuple[int, str, str]]]
    ) -> None:
        table.setRowCount(0)
        table.setRowCount(len(data))

        if not data:
            return

        num_columns: int = len(data[0])
        table.setColumnCount(num_columns)

        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                table.setItem(row_index, col_index, item)

    def load_last_results(self, file_name: str) -> None:
        """load every tables with last check data, and show
        last modified date

        Args:
            file_name (str): name of the file
        """
        results: list[list[Any]]
        date: list[str]
        results, date = json_man.load_result_process(process.id_current_game - 1, file_name)
        self.update_table(self.ui.tableWidget_1, [(row[0], row[1]) for row in results[0]])
        self.update_table(self.ui.tableWidget_2, [(row[0], row[1]) for row in results[1]])
        self.update_table(self.ui.tableWidget_3, [(row[0], row[1]) for row in results[2]])

        self.ui.label_lastUdate_1.setText(date[0])
        self.ui.label_lastUdate_2.setText(date[1])
        self.ui.label_lastUdate_3.setText(date[2])

        # languageTool
        process.list_languagetool_current_file_rules = [row[2] for row in results[1]]

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        # pushButton
        self.ui.pushButton_gameDictionary.clicked.connect(self.pushbutton_gamedictionary_clicked)
        self.ui.pushButton_method_1.clicked.connect(self.pushbutton_method_1_clicked)
        self.ui.pushButton_method_2.clicked.connect(self.pushbutton_method_2_clicked)
        self.ui.pushButton_method_3.clicked.connect(self.pushbutton_method_3_clicked)
        self.ui.pushButton_uploadSpecificWords.clicked.connect(self.pushbutton_uploadspecificwords_clicked)
        # lineEdit
        self.ui.lineEdit_urlSheet.textChanged.connect(self.lineedit_urlsheet_textchanged)
        self.urlsheet_timer.timeout.connect(self.check_urlsheet_access)
        self.ui.lineEdit_frenchColumn.textChanged.connect(self.lineedit_frenchcolumn_textchanged)
        # comboBox
        self.ui.comboBox_game.currentIndexChanged.connect(self.combobox_game_currentindexchanged)
        # tab
        self.ui.tableWidget_1.customContextMenuRequested.connect(self.tablewidget_1_contextmenu)
        self.ui.tableWidget_2.customContextMenuRequested.connect(self.tablewidget_2_contextmenu)
        # thread start
        self.m_worker.signal_load_word_excluded_start.connect(self.m_worker.load_excluded_word_in_table_thread)
        self.m_worker.signal_get_name_sheet_start.connect(self.m_worker.get_name_sheet_thread)
        self.m_worker.signal_orthocheck_load_dictionary_start.connect(self.m_worker.orthocheck_load_dictionary_thread)
        self.m_worker.signal_languagetool_initialize_start.connect(self.m_worker.languagetool_initialize_thread)
        self.m_worker.signal_orthocheck_process_start.connect(self.m_worker.orthocheck_process_thread)
        self.m_worker.signal_language_tool_process_start.connect(self.m_worker.language_tool_process_thread)
        self.m_worker.signal_word_check_process_start.connect(self.m_worker.word_check_process_thread)
        self.m_worker.signal_add_specific_words_start.connect(self.m_worker.add_specific_words_thread)
        # thread finish
        self.m_worker.signal_load_word_excluded_finished.connect(self.load_dialog_finished)
        self.m_worker.signal_get_name_sheet_finished.connect(self.get_name_sheet_finished)
        self.m_worker.signal_orthocheck_load_dictionary_finished.connect(self.orthocheck_load_dictionary_finished)
        self.m_worker.signal_languagetool_initialize_finished.connect(self.languagetool_initialize_finished)
        self.m_worker.signal_orthocheck_process_finished.connect(self.orthocheck_process_finished)
        self.m_worker.signal_language_tool_process_finished.connect(self.language_tool_process_finished)
        self.m_worker.signal_word_check_process_finished.connect(self.word_check_process_finished)
        self.m_worker.signal_add_specific_words_finished.connect(self.add_specific_words_finished)
        # help

    def pushbutton_gamedictionary_clicked(self) -> None:
        """slot for pushButton_gameDictionary
        """
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.ui.pushButton_gameDictionary.setEnabled(False)
        self.m_worker.signal_load_word_excluded_start.emit(self.ui.comboBox_game.currentIndex()-1)

    def pushbutton_method_1_clicked(self) -> None:
        """slot for pushButton_method_1
        """
        self.ui.pushButton_method_1.setEnabled(False)
        if not self.is_orthocheck_available:
            self.m_worker.signal_orthocheck_load_dictionary_start.emit()
        self.m_worker.signal_orthocheck_process_start.emit(self.ui.lineEdit_urlSheet.text(),
                                                           self.ui.lineEdit_frenchColumn.text())

    def pushbutton_method_2_clicked(self) -> None:
        """slot for pushButton_method_2
        """
        self.ui.pushButton_method_2.setEnabled(False)
        if not self.is_languagetool_available:
            self.m_worker.signal_languagetool_initialize_start.emit()
        self.m_worker.signal_language_tool_process_start.emit(self.ui.lineEdit_urlSheet.text(),
                                                              self.ui.lineEdit_frenchColumn.text())

    def pushbutton_method_3_clicked(self) -> None:
        """slot for pushButton_method_3
        """
        self.ui.pushButton_method_3.setEnabled(False)
        self.m_worker.signal_word_check_process_start.emit(self.ui.lineEdit_urlSheet.text(),
                                                           self.ui.lineEdit_frenchColumn.text())

    def pushbutton_uploadspecificwords_clicked(self) -> None:
        """slot for pushButton_uploadSpecificWords
        """
        self.ui.pushButton_uploadSpecificWords.setEnabled(False)
        self.m_worker.signal_add_specific_words_start.emit()

    def lineedit_urlsheet_textchanged(self) -> None:
        """slot for lineEdit_urlSheet
        """
        self.ui.lineEdit_urlSheet.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ui.label_sheetOpened.setText("")
        self.ui.label_lastUdate_1.setText("")
        self.ui.label_lastUdate_2.setText("")
        self.ui.label_lastUdate_3.setText("")
        text: str = self.ui.lineEdit_urlSheet.text()
        self.is_url_correct = False
        if len(text) > 0:
            self.urlsheet_timer.start()
        else:
            self.toggle_ui_enabled_buttons_methods(False)
            self.toggle_ui_enabled_tabWidget_result(False)

    def check_urlsheet_access(self) -> None:
        """Vérifier l'accès à l'élément après un délai"""
        text: str = self.ui.lineEdit_urlSheet.text()
        self.m_worker.signal_get_name_sheet_start.emit(text)

    def lineedit_frenchcolumn_textchanged(self, text: str) -> None:
        """slot for lineEdit_frenchColumn
        """

    def combobox_game_currentindexchanged(self, index: int) -> None:
        """slot for comboBox_game
        """
        self.toggle_ui_enabled_except_combobox_game(bool(index))
        self.ui.lineEdit_frenchColumn.setText(json_man.data_json[index - 1]["column_sheet"])  # type: ignore
        process.set_id_and_word_list(index, [])
        if len(self.ui.lineEdit_urlSheet.text()) > 0:
            self.urlsheet_timer.start()

    def tablewidget_1_contextmenu(self, pos: QPoint) -> None:
        """slot for tableWidget_excludedWords
        """
        item: QTableWidgetItem = self.ui.tableWidget_1.itemAt(pos)
        if item is None:  # type: ignore
            return
        menu = QMenu(self)

        self.add_to_specific_dictionary_action = QAction("Ajouter aux termes du jeu", self)
        self.add_to_global_dictionary_action = QAction("Ajouter au dictionnaire de la méthode", self)
        self.delete_action = QAction("Faute traitée", self)
        self.add_character_action = QAction("Ajouter le caractère", self)
        self.add_punctuation_action = QAction("Ajouter la ponctuation", self)

        self.add_to_specific_dictionary_action.triggered.connect(lambda: self.add_to_specific_dictionary(item))
        self.add_to_global_dictionary_action.triggered.connect(lambda: self.add_to_global_dictionary(item))
        self.delete_action.triggered.connect(lambda: self.delete_item(item))
        self.add_character_action.triggered.connect(lambda: self.add_character(item))
        self.add_punctuation_action.triggered.connect(lambda: self.add_punctuation(item))

        if item.text().endswith(", caractère non autorisé"):
            menu.addAction(self.add_character_action)
            menu.addAction(self.add_punctuation_action)
        else:
            menu.addAction(self.add_to_specific_dictionary_action)
            menu.addAction(self.add_to_global_dictionary_action)
            menu.addSeparator()
            menu.addAction(self.delete_action)
        menu.exec_(self.ui.tableWidget_1.viewport().mapToGlobal(pos))

    def tablewidget_2_contextmenu(self, pos: QPoint) -> None:
        """slot for tableWidget_excludedWords
        """
        item: QTableWidgetItem = self.ui.tableWidget_2.itemAt(pos)
        if item is None:  # type: ignore
            return
        menu = QMenu(self)

        rule_text: str = process.list_languagetool_current_file_rules[item.row()]
        self.add_to_ignored_rules_action = QAction("ignorer " + rule_text + " pour ce jeu", self)
        self.delete_languagetool_item_action = QAction("Faute traitée", self)

        self.add_to_ignored_rules_action.triggered.connect(lambda: self.add_to_ignored_rules(item))
        self.delete_languagetool_item_action.triggered.connect(lambda: self.delete_languagetool_item(item))

        menu.addAction(self.add_to_ignored_rules_action)
        menu.addSeparator()
        menu.addAction(self.delete_languagetool_item_action)

        menu.exec_(self.ui.tableWidget_2.viewport().mapToGlobal(pos))

    def load_dialog_finished(self) -> None:
        """slot for signal load_dialog_finished
        """
        QApplication.restoreOverrideCursor()
        self.dialog_dict = DialogExcludedWords()
        self.dialog_dict.load_excluded_word_in_table()
        self.dialog_dict.exec()
        self.ui.pushButton_gameDictionary.setEnabled(True)

    def get_name_sheet_finished(self, result: str | int) -> None:
        """slot for signal get_name_sheet_finished
        """
        self.is_url_correct = isinstance(result, str)
        if self.is_url_correct:
            self.ui.lineEdit_urlSheet.setStyleSheet("background-color: rgb(0, 200, 0);")
            self.toggle_ui_enabled_buttons_methods(True)
            self.toggle_ui_enabled_tabWidget_result(True)
            self.ui.label_sheetOpened.setText(str(result))
            self.load_last_results(str(result))
        else:
            self.ui.lineEdit_urlSheet.setStyleSheet("background-color: rgb(200, 0, 0);")
            self.toggle_ui_enabled_buttons_methods(False)
            self.toggle_ui_enabled_tabWidget_result(False)
            self.ui.label_sheetOpened.setText("url incorrect")

    def orthocheck_load_dictionary_finished(self) -> None:
        """slot for signal orthocheck_load_dictionary_finished
        """
        self.is_orthocheck_available = True
        # self.ui.pushButton_method_1.setEnabled(bool(self.ui.comboBox_game.currentIndex() and self.is_url_correct))

    def languagetool_initialize_finished(self) -> None:
        """slot for signal languagetool_initialize_finished
        """
        self.is_languagetool_available = True
        # self.ui.pushButton_method_2.setEnabled(bool(self.ui.comboBox_game.currentIndex() and self.is_url_correct))

    def orthocheck_process_finished(self, result: list[tuple[int, str]] | int) -> None:
        """slot for signal orthocheck_process_finished
        """
        self.ui.pushButton_method_1.setEnabled(True)
        if isinstance(result, int):
            # TODO
            pass
        else:
            self.update_table(self.ui.tableWidget_1, result)

            json_man.save_result_process_one_str(process.id_current_game - 1,
                                                 self.ui.label_sheetOpened.text(), 1, result)
            self.ui.label_lastUdate_1.setText(process.get_current_date())

    def language_tool_process_finished(self, result: list[tuple[int, str, str]] | int) -> None:
        """slot for signal language_tool_process_finished
        """
        self.ui.pushButton_method_2.setEnabled(True)
        if isinstance(result, int):
            # TODO
            pass
        else:
            self.update_table(self.ui.tableWidget_2, [(row[0], row[1]) for row in result])
            process.list_languagetool_current_file_rules = [row[2] for row in result]

            json_man.save_result_process_two_str(process.id_current_game - 1,
                                                 self.ui.label_sheetOpened.text(), 2, result)
            self.ui.label_lastUdate_2.setText(process.get_current_date())

    def word_check_process_finished(self, result: list[tuple[int, str]] | int) -> None:
        """slot for signal language_tool_process_finished
        """
        self.ui.pushButton_method_3.setEnabled(True)
        if isinstance(result, int):
            # TODO
            pass
        else:
            self.update_table(self.ui.tableWidget_3, result)

            json_man.save_result_process_one_str(process.id_current_game - 1,
                                                 self.ui.label_sheetOpened.text(), 3, result)
            self.ui.label_lastUdate_3.setText(process.get_current_date())

    def add_specific_words_finished(self) -> None:
        """slot for signal add_specific_words_finished
        """
        self.ui.pushButton_uploadSpecificWords.setEnabled(True)
        self.ui.pushButton_uploadSpecificWords.setText("Pas de termes à uploader")
        self.ui.comboBox_game.setEnabled(True)
        self.ui.pushButton_gameDictionary.setEnabled(True)
        self.ui.comboBox_game.setToolTip("")
        self.ui.pushButton_gameDictionary.setToolTip("")

    def closeEvent(self, a0: QCloseEvent) -> None:
        process.language_tool_close()
        if len(process.list_specific_word_to_upload) > 0:
            self.exit_widget = ConfirmExit()
            self.exit_widget.exec()
        self.urlsheet_timer.stop()
        if self.m_thread.isRunning():
            self.m_thread.quit()
            self.m_thread.wait()
        a0.accept()
