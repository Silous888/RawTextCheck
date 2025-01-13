
# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMenu, QAction
from PyQt5.QtCore import QPoint

# -------------------- Import Lib User -------------------
from qt_files.Ui_dialog_excluded_words import Ui_Dialog
import process


class DialogExcludedWords(QDialog):

    def __init__(self) -> None:
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  # type: ignore
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

    def save_excluded_word(self) -> None:
        """save excluded word in the sheet
        """
        excluded_words: list[str] = []
        for row in range(self.ui.tableWidget_excludedWords.rowCount()-1):
            item: QTableWidgetItem = self.ui.tableWidget_excludedWords.item(row, 0)
            excluded_words.append(item.text())
        process.set_list_specific_word(excluded_words)

    def delete_item(self, item: QTableWidgetItem) -> None:
        """Delete the selected item from the table.

        Args:
            item (QTableWidgetItem): item from the table
        """
        self.ui.tableWidget_excludedWords.removeRow(item.row())

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        self.ui.pushButton_resetChange.clicked.connect(self.pushbutton_resetchange_clicked)
        self.ui.pushButton_saveAndQuit.clicked.connect(self.pushbutton_saveandquit_clicked)

        self.ui.tableWidget_excludedWords.customContextMenuRequested.connect(self.tablewidget_excludedwords_contextmenu)
        self.ui.tableWidget_excludedWords.itemChanged.connect(self.handle_item_changed)

    def pushbutton_resetchange_clicked(self) -> None:
        """slot for pushButton_resetChanges
        """
        self.ui.tableWidget_excludedWords.setRowCount(0)
        self.load_excluded_word_in_table()

    def pushbutton_saveandquit_clicked(self) -> None:
        """slot for pushButton_saveAndQuit
        """

        self.save_excluded_word()
        self.close()

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
