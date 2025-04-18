"""start file of the application"""
# -------------------- Import Lib Standard -------------------
import sys

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

# -------------------- Import Lib User -------------------
from windows_logic.mainwindow import MainWindow
import json_management

# pyinstaller --onefile --noconsole --name FautesCheck --icon=./ressource/DreamteamLogo.ico main.py

# -------------------- Main code -------------------
if __name__ == "__main__":
    # load data
    json_management.load_json()

    # create qt application
    app = QApplication(sys.argv)
    program = MainWindow()

    apply_stylesheet(app, theme='dark_amber.xml')

    program.show()
    sys.exit(app.exec())
