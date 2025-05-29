from PyQt5.QtCore import QObject

from checkfrench.script import json_projects


class WorkerProjectManager(QObject):

    data_comboBox_project: list[tuple[int, str]] = []

    def __init__(self) -> None:
        super().__init__()
