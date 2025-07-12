"""
File        : dataresult_tableview.py
Author      : Silous
Created on  : 2025-07-12
Description :
"""

# == Imports ==================================================================

from typing import List
from PyQt5.QtWidgets import QTableView, QMenu, QAction, QWidget
from PyQt5.QtCore import QAbstractItemModel, QItemSelectionModel, QModelIndex, Qt, QPoint
from PyQt5.QtGui import QKeyEvent


# == Classes ==================================================================

class DataResultTableView(QTableView):
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
        self._column_visibility: dict[int, bool] = {}

        horizontal_header: QWidget | None = self.horizontalHeader()
        if horizontal_header is not None:
            horizontal_header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            horizontal_header.customContextMenuRequested.connect(self.show_context_menu)

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        """Handle key press events.
        Args:
            e (QKeyEvent | None): The key event to handle.
        """
        if e is None:
            return
        if e.key() == Qt.Key.Key_Delete:
            self.delete_selected_row()
        else:
            super().keyPressEvent(e)

    def show_context_menu(self, position: QPoint) -> None:
        """Show the context menu at the specified position.
        Args:
            position (QPoint): The position where the context menu should be displayed.
        """

        model: QAbstractItemModel | None = self.model()
        if model is None:
            return

        menu = QMenu(self)

        # Action: Delete rows if selection
        selection_model: QItemSelectionModel | None = self.selectionModel()
        if selection_model and selection_model.selectedRows():
            delete_action = QAction(self.tr("Delete"), self)
            delete_action.triggered.connect(self.delete_selected_row)
            menu.addAction(delete_action)  # type: ignore
            menu.addSeparator()

        visibility_menu = QMenu("Visibility", self)
        # Action: Toggle column visibility
        for col in range(model.columnCount()):
            col_name = model.headerData(col, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
            if col_name is None:
                col_name = f"Column {col}"

            action = QAction(str(col_name), self)
            action.setCheckable(True)
            is_visible: bool = not self.isColumnHidden(col)
            self._column_visibility[col] = is_visible
            action.setChecked(is_visible)
            action.triggered.connect(lambda checked, c=col: self.toggle_column_visibility(c, checked))  # type: ignore
            visibility_menu.addAction(action)  # type: ignore

        menu.addMenu(visibility_menu)

        viewport: QWidget | None = self.viewport()
        if viewport is not None:
            menu.exec_(viewport.mapToGlobal(position))

    def toggle_column_visibility(self, column: int, visible: bool) -> None:
        """Toggle visibility of a given column."""
        self.setColumnHidden(column, not visible)
        self._column_visibility[column] = visible

    def delete_selected_row(self) -> None:
        """Delete the selected rows from the model.
        This method retrieves the selected rows from the model and removes them.
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
        model.removeRow(selection[0].row())
