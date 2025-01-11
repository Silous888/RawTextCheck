# -------------------- Import Lib Standard -------------------
import sys

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QApplication

# -------------------- Import Lib User -------------------
from mainwindow import MainWindow

# pyinstaller --onefile --noconsole --name FautesCheck --icon=./ressource/DreamteamLogo.ico main.py

# -------------------- Main code -------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    program = MainWindow()
    program.show()
    sys.exit(app.exec())
