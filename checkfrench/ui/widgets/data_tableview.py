"""
File        : data_tableview.py
Author      : Silous
Created on  : 2025-05-31
Description : Custom QTableView with context menu and delete functionality.

This module defines a custom QTableView that supports right-click context menus
and allows users to delete selected rows using the Delete key or through the context menu.
"""

# == Imports ==================================================================

from typing import List
from PyQt5.QtWidgets import QTableView, QMenu, QAction, QWidget
from PyQt5.QtCore import QAbstractItemModel, QItemSelectionModel, QModelIndex, Qt, QPoint
from PyQt5.QtGui import QKeyEvent


# == Classes ==================================================================

class DataTableView(QTableView):
    """Custom QTableView with context menu and delete functionality.
    This class extends QTableView to provide a context menu for deleting selected rows
    and handles the Delete key press event to remove selected rows.
    """
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the DataTableView.
        Args:
            parent (QWidget | None): The parent widget for this table view.
        """
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        """Handle key press events.
        Args:
            e (QKeyEvent | None): The key event to handle.
        """
        if e is None:
            return
        if e.key() == Qt.Key.Key_Delete:
            self.delete_selected_rows()
        else:
            super().keyPressEvent(e)

    def show_context_menu(self, position: QPoint) -> None:
        """Show the context menu at the specified position.
        Args:
            position (QPoint): The position where the context menu should be displayed.
        """

        # Get the selected rows from the selection model
        selection_model: QItemSelectionModel | None = self.selectionModel()
        if selection_model is None:
            return
        selection: List[QModelIndex] = selection_model.selectedRows()
        if not selection:
            return

        # Create the context menu
        menu: QMenu = QMenu(self)
        delete_action = QAction(self.tr("Delete"), self)
        delete_action.triggered.connect(self.delete_selected_rows)
        menu.addAction(delete_action)  # type: ignore

        # Show the context menu at the global position
        viewport: QWidget | None = self.viewport()
        if viewport is not None:
            menu.exec_(viewport.mapToGlobal(position))

    def delete_selected_rows(self) -> None:
        """Delete the selected rows from the model.
        This method retrieves the selected rows from the model and removes them.
        It avoids deleting the last empty row to maintain the table structure.
        """
        # Get the model and selection model
        model: QAbstractItemModel | None = self.model()
        if model is None:
            return
        selection_model: QItemSelectionModel | None = self.selectionModel()
        if selection_model is None:
            return
        selection: List[QModelIndex] = selection_model.selectedRows()
        if not selection:
            return

        # Collect the rows to delete, sorted in reverse order to avoid index issues while deleting rows
        rows_to_delete: List[int] = sorted([index.row() for index in selection if index.row()], reverse=True)

        for row in rows_to_delete:
            if row < model.rowCount() - 1:  # Avoid deleting the last empty row
                model.removeRow(row)
