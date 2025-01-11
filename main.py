"""start file of the application"""
# -------------------- Import Lib Standard -------------------
import sys

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QApplication

# -------------------- Import Lib User -------------------
from windows_logic.mainwindow import MainWindow
import process

# pyinstaller --onefile --noconsole --name FautesCheck --icon=./ressource/DreamteamLogo.ico main.py

# -------------------- Main code -------------------
if __name__ == "__main__":
    # load data
    process.data_json = process.load_json()

    # create qt application
    app = QApplication(sys.argv)
    program = MainWindow()
    program.show()
    sys.exit(app.exec())
