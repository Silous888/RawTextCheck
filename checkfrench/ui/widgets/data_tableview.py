from typing import List
from PyQt5.QtWidgets import QTableView, QMenu, QAction, QWidget
from PyQt5.QtCore import QAbstractItemModel, QItemSelectionModel, QModelIndex, Qt, QPoint
from PyQt5.QtGui import QKeyEvent


class DataTableView(QTableView):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        if e is None:
            return
        if e.key() == Qt.Key.Key_Delete:
            self.delete_selected_rows()
        else:
            super().keyPressEvent(e)

    def show_context_menu(self, position: QPoint) -> None:
        selection_model: QItemSelectionModel | None = self.selectionModel()
        if selection_model is None:
            return
        selection: List[QModelIndex] = selection_model.selectedRows()
        if not selection:
            return

        menu: QMenu = QMenu(self)
        delete_action = QAction(self.tr("Delete"), self)
        delete_action.triggered.connect(self.delete_selected_rows)
        menu.addAction(delete_action)  # type: ignore

        viewport: QWidget | None = self.viewport()
        if viewport is not None:
            menu.exec_(viewport.mapToGlobal(position))

    def delete_selected_rows(self) -> None:
        model: QAbstractItemModel | None = self.model()
        if model is None:
            return
        selection_model: QItemSelectionModel | None = self.selectionModel()
        if selection_model is None:
            return
        selection: List[QModelIndex] = selection_model.selectedRows()
        if not selection:
            return

        rows_to_delete: List[int] = sorted([index.row() for index in selection if index.row()], reverse=True)

        for row in rows_to_delete:
            if row < model.rowCount() - 1:  # Avoid deleting the last empty row
                model.removeRow(row)
