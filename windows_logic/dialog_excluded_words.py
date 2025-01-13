
# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMenu, QAction, QApplication
from PyQt5.QtCore import Qt, QObject, QPoint, QThread, pyqtSignal, pyqtSlot  # type: ignore

# -------------------- Import Lib User -------------------
from qt_files.Ui_dialog_excluded_words import Ui_Dialog
import process


class _WorkerDialogExcludedWords(QObject):

    signal_set_list_specific_word_start = pyqtSignal(list)

    signal_set_list_specific_word_finished = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    @pyqtSlot(list)
    def set_list_specific_word_thread(self, excluded_words: list[str]) -> None:
        process.set_list_specific_word(excluded_words)
        self.signal_set_list_specific_word_finished.emit()


class DialogExcludedWords(QDialog):

    def __init__(self) -> None:
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  # type: ignore

        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = _WorkerDialogExcludedWords()
        self.m_worker.moveToThread(self.m_thread)

        self.set_up_connect()

        self.ui.tableWidget_excludedWords.installEventFilter(self)

    def load_excluded_word_in_table(self) -> None:
        """load excluded word in the table
        """
        self.manual_change = False
        for word in process.list_excluded_word_current_game:
            self.ui.tableWidget_excludedWords.insertRow(self.ui.tableWidget_excludedWords.rowCount())
            item = QTableWidgetItem(word)
            self.ui.tableWidget_excludedWords.setItem(self.ui.tableWidget_excludedWords.rowCount()-1, 0, item)
        self.ui.tableWidget_excludedWords.insertRow(self.ui.tableWidget_excludedWords.rowCount())
        self.manual_change = True

    def get_to_save_excluded_word(self) -> list[str]:
        """save excluded word in the sheet
        """
        excluded_words: list[str] = []
        for row in range(self.ui.tableWidget_excludedWords.rowCount()-1):
            item: QTableWidgetItem = self.ui.tableWidget_excludedWords.item(row, 0)
            excluded_words.append(item.text())

        return excluded_words

    def delete_item(self, item: QTableWidgetItem) -> None:
        """Delete the selected item from the table.

        Args:
            item (QTableWidgetItem): item from the table
        """
        self.ui.tableWidget_excludedWords.removeRow(item.row())

    def toggle_ui_enable(self, enable: bool) -> None:
        self.ui.pushButton_resetChange.setEnabled(enable)
        self.ui.pushButton_saveAndQuit.setEnabled(enable)
        self.ui.tableWidget_excludedWords.setEnabled(enable)

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        # pushButton
        self.ui.pushButton_resetChange.clicked.connect(self.pushbutton_resetchange_clicked)
        self.ui.pushButton_saveAndQuit.clicked.connect(self.pushbutton_saveandquit_clicked)
        # tableWidget
        self.ui.tableWidget_excludedWords.customContextMenuRequested.connect(self.tablewidget_excludedwords_contextmenu)
        self.ui.tableWidget_excludedWords.itemChanged.connect(self.handle_item_changed)
        # thread start
        self.m_worker.signal_set_list_specific_word_start.connect(
            self.m_worker.set_list_specific_word_thread)  # type: ignore
        # thread finished
        self.m_worker.signal_set_list_specific_word_finished.connect(self.set_list_specific_word_finished)

    def pushbutton_resetchange_clicked(self) -> None:
        """slot for pushButton_resetChanges
        """
        self.ui.tableWidget_excludedWords.setRowCount(0)
        self.load_excluded_word_in_table()

    def pushbutton_saveandquit_clicked(self) -> None:
        """slot for pushButton_saveAndQuit
        """
        self.toggle_ui_enable(False)
        excluded_words: list[str] = self.get_to_save_excluded_word()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.m_worker.signal_set_list_specific_word_start.emit(excluded_words)

    def tablewidget_excludedwords_contextmenu(self, pos: QPoint) -> None:
        """slot for tableWidget_excludedWords
        """
        item: QTableWidgetItem = self.ui.tableWidget_excludedWords.itemAt(pos)
        if item is None:  # type: ignore
            return
        menu = QMenu(self)

        self.delete_action = QAction("Delete", self)
        self.delete_action.triggered.connect(lambda: self.delete_item(item))

        menu.addAction(self.delete_action)
        menu.exec_(self.ui.tableWidget_excludedWords.viewport().mapToGlobal(pos))

    def handle_item_changed(self, item: QTableWidgetItem) -> None:
        """Handle changes to items in the table.

        Args:
            item (QTableWidgetItem): The item that was changed.
        """
        if not self.manual_change:
            return
        if item.row() == self.ui.tableWidget_excludedWords.rowCount() - 1:
            if len(item.text()) > 0:
                self.ui.tableWidget_excludedWords.insertRow(self.ui.tableWidget_excludedWords.rowCount())
        elif len(item.text()) == 0:
            self.delete_item(item)

    def set_list_specific_word_finished(self) -> None:
        QApplication.restoreOverrideCursor()
        self.toggle_ui_enable(True)
        self.close()
