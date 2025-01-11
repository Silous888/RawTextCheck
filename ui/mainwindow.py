"""functions of the UI"""

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QObject, QThread

# -------------------- Import Lib User -------------------
from ui.Ui_mainwindow import Ui_MainWindow
import process


# -------------------------------------------------------------------#
#                          CLASS WORKER                              #
# -------------------------------------------------------------------#
class _Worker(QObject):

    def __init__(self) -> None:
        super().__init__()


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
        for game in process.data:
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
        self.ui.lineEdit_urlSheet.textChanged.connect(self.lineedit_urlsheet_textchanged)
        self.ui.lineEdit_frenchColumn.textChanged.connect(self.lineedit_frenchcolumn_textchanged)
        # comboBox
        self.ui.comboBox_game.currentIndexChanged.connect(self.combobox_game_currentindexchanged)

    def pushbutton_gamedictionary_clicked(self) -> None:
        """slot for pushButton_gameDictionary
        """

    def pushbutton_method_1_clicked(self) -> None:
        """slot for pushButton_method_1
        """

    def pushbutton_method_2_clicked(self) -> None:
        """slot for pushButton_method_2
        """

    def pushbutton_method_3_clicked(self) -> None:
        """slot for pushButton_method_3
        """

    def lineedit_urlsheet_textchanged(self, text: str) -> None:
        """slot for lineEdit_urlSheet
        """

    def lineedit_frenchcolumn_textchanged(self, text: str) -> None:
        """slot for lineEdit_frenchColumn
        """

    def combobox_game_currentindexchanged(self, index: int) -> None:
        """slot for comboBox_game
        """
        self.toggle_ui_enabled_except_combobox_game(bool(index))
