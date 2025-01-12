
# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint

# -------------------- Import Lib User -------------------
from qt_files.Ui_dialog_excluded_words import Ui_Dialog
import process


class DialogExcludedWords(QDialog):

    def __init__(self, id_game: int) -> None:
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  # type: ignore
        self.set_up_connect()
        self.id_game: int = id_game

    def load_excluded_word_in_table(self) -> None:
        """load excluded word in the table
        """
        list_excluded_word: list[str] | int = process.get_list_specific_word(sheet_index=self.id_game)
        if isinstance(list_excluded_word, int):
            return
        for word in list_excluded_word:
            self.ui.tableWidget_excludedWords.insertRow(self.ui.tableWidget_excludedWords.rowCount())
            item = QTableWidgetItem(word)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # type: ignore
            self.ui.tableWidget_excludedWords.setItem(self.ui.tableWidget_excludedWords.rowCount()-1, 0, item)

    def save_excluded_word(self) -> None:
        """save excluded word in the sheet
        """
        excluded_words: list[str] = []
        for row in range(self.ui.tableWidget_excludedWords.rowCount()):
            item: QTableWidgetItem = self.ui.tableWidget_excludedWords.item(row, 0)
            excluded_words.append(item.text())
            process.set_list_specific_word(self.id_game, excluded_words)

    def set_up_connect(self) -> None:
        """connect slots and signals
        """
        self.ui.pushButton_resetChange.clicked.connect(self.pushbutton_resetchange_clicked)
        self.ui.pushButton_saveAndQuit.clicked.connect(self.pushbutton_saveandquit_clicked)
        self.ui.tableWidget_excludedWords.customContextMenuRequested.connect(self.tablewidget_excludedwords_contextmenu)

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
        # Créer un menu contextuel
        menu = QMenu(self)

        # Ajouter des actions au menu
        self.edit_action = QAction("Edit", self)
        self.delete_action = QAction("Delete", self)

        # Connecter les actions à des méthodes
        self.edit_action.triggered.connect(lambda: self.edit_item(item))
        self.delete_action.triggered.connect(lambda: self.delete_item(item))

        # Ajouter les actions au menu
        menu.addAction(self.edit_action)
        menu.addAction(self.delete_action)

        # Afficher le menu contextuel à l'endroit du clic
        menu.exec_(self.ui.tableWidget_excludedWords.viewport().mapToGlobal(pos))

    def edit_item(self, item: QTableWidgetItem) -> None:
        print(f"Edit item: {item.text()}")

    def delete_item(self, item: QTableWidgetItem) -> None:
        print(f"Delete item: {item.text()}")
