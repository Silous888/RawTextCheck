
# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QDialog

# -------------------- Import Lib User -------------------
from qt_files.Ui_dialog_excluded_words import Ui_Dialog


class DialogExcludedWords(QDialog):

    def __init__(self) -> None:
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  # type: ignore
