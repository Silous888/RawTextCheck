"""
File        : dataresult_tableview.py
Author      : Silous
Created on  : 2025-07-12
Description :
"""

# == Imports ==================================================================

from typing import List
from PyQt5.QtWidgets import QTableView, QMenu, QAction, QWidget, QApplication
from PyQt5.QtCore import QAbstractItemModel, QItemSelectionModel, QModelIndex, Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QKeyEvent


# == Classes ==================================================================

class DataResultTableView(QTableView):
    """Custom QTableView with context menu and delete functionality.
    This class extends QTableView to provide a context menu for deleting selected rows
    and handles the Delete key press event to remove selected rows.
    Attributes:
        custom_context_action_requested (pyqtSignal): signal to add action to contextmenu
    """

    custom_context_actions_requested = pyqtSignal(QMenu)

    _columns_to_hide_by_default: list[str] = []

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the DataTableView.
        Args:
            parent (QWidget | None): The parent widget for this table view.
        """
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self._column_visibility: dict[int, bool] = {}
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)

        horizontal_header: QWidget | None = self.horizontalHeader()
        if horizontal_header is not None:
            horizontal_header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            horizontal_header.customContextMenuRequested.connect(self.show_context_menu)

    def setModel(self, model: QAbstractItemModel | None) -> None:
        """override setModel to hide by default some column

        Args:
            model (QAbstractItemModel | None): model
        """
        super().setModel(model)

        if model is None:
            return
        # Apply default hiding logic once model is set
        for col in range(model.columnCount()):
            header = model.headerData(col, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
            if header in self._columns_to_hide_by_default:
                self.setColumnHidden(col, True)

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

        selection_model: QItemSelectionModel | None = self.selectionModel()
        selected_rows: List[QModelIndex] = selection_model.selectedRows() if selection_model else []

        if selected_rows:
            row: int = selected_rows[0].row()

            # Action: Delete
            delete_action = QAction(self.tr("Delete"), self)
            delete_action.triggered.connect(self.delete_selected_row)
            menu.addAction(delete_action)  # type: ignore
            menu.addSeparator()

            # Get data for the selected row to populate the Copy submenu
            idx = lambda col: model.index(row, col)  # type: ignore
            line: str      = model.data(idx(1), Qt.ItemDataRole.DisplayRole)
            error: str     = model.data(idx(2), Qt.ItemDataRole.DisplayRole)
            # error_type: str = model.data(idx(3), Qt.ItemDataRole.DisplayRole)
            suggestion: str = model.data(idx(5), Qt.ItemDataRole.DisplayRole)


            copy_line_action = QAction(self.tr("Copy text"), self)
            copy_line_action.triggered.connect(lambda: QApplication.clipboard().setText(str(line)))  # type: ignore
            menu.addAction(copy_line_action)  # type: ignore

            copy_error_action = QAction(self.tr("Copy error"), self)
            copy_error_action.triggered.connect(lambda: QApplication.clipboard().setText(str(error)))  # type: ignore
            menu.addAction(copy_error_action)  # type: ignore


            if suggestion:
                suggestion_menu = QMenu(self.tr("Copy suggestion"), self)
                suggestions: list[str] = [s.strip().strip("'") for s in str(suggestion).split(",") if s.strip()]
                if suggestions:
                    suggestion_menu.addSeparator()
                    for sug in suggestions:
                        sug_action = QAction(sug, self)
                        sug_action.triggered.connect(lambda checked, s=sug: QApplication.clipboard().setText(s))  # type: ignore
                        suggestion_menu.addAction(sug_action)  # type: ignore

                menu.addMenu(suggestion_menu)
            menu.addSeparator()

        self.custom_context_actions_requested.emit(menu)

        visibility_menu = QMenu(self.tr("Visibility"), self)
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

    def set_columns_hidden_by_default(self, column_names: list[str]) -> None:
        """Set columns (by header name) to hide once the model is set."""
        self._columns_to_hide_by_default = column_names

    def get_hidden_columns_labels(self) -> list[str]:
        """Return the list of column labels that are currently hidden."""
        labels: list[str] = []
        model: QAbstractItemModel | None = self.model()
        if model is None:
            return labels

        for col in range(model.columnCount()):
            if self.isColumnHidden(col):
                header_data = model.headerData(col, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
                label: str = str(header_data) if header_data is not None else f"Column {col}"
                labels.append(label)

        return labels

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
