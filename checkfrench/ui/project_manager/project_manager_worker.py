from PyQt5.QtCore import QObject


class WorkerProjectManager(QObject):

    data_comboBox_project: list[tuple[int, str]] = []

    def __init__(self) -> None:
        super().__init__()
