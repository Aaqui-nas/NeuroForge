from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from neuroforge.graph.components import ComponentLibrary
from neuroforge.graph.registry import NodeRegistry


class NodePalette(QWidget):
    """Side-panel listing built-in node types and custom components.

    Built-in nodes are grouped by category (from `NodeRegistry`). Custom
    components appear under a dedicated "Composants" section. Call `refresh()`
    after adding a component to update the panel.

    Double-clicking a built-in node emits `node_type_activated` with the
    registry type string (e.g. ``"linear"``). Double-clicking a component
    emits ``"component:<id>"``.

    Attributes:
        node_type_activated: Emitted with the type key when the user activates
            an entry.
    """

    node_type_activated: Signal = Signal(str)

    def __init__(
        self,
        registry: NodeRegistry,
        library: ComponentLibrary | None = None,
    ) -> None:
        """Build the palette.

        Args:
            registry: Built-in node registry.
            library: Optional component library; if provided, a "Composants"
                section is shown and kept up-to-date via `refresh()`.
        """
        super().__init__()
        self._registry = registry
        self._library = library

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Rechercher…")
        self._search.setClearButtonEnabled(True)
        layout.addWidget(self._search)

        self._tree = QTreeWidget()
        self._tree.setHeaderHidden(True)
        self._tree.setIndentation(12)
        layout.addWidget(self._tree)

        self._populate()
        self._search.textChanged.connect(self._filter)
        self._tree.itemDoubleClicked.connect(self._on_double_click)

    def refresh(self) -> None:
        """Re-populate the palette. Call after registering a new component."""
        query = self._search.text()
        self._populate()
        if query:
            self._filter(query)

    def _populate(self) -> None:
        self._tree.clear()
        for category in sorted(self._registry.categories()):
            cat_item = QTreeWidgetItem([category])
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self._tree.addTopLevelItem(cat_item)
            for defn in sorted(self._registry.by_category(category), key=lambda d: d.display_name):
                node_item = QTreeWidgetItem([defn.display_name])
                node_item.setData(0, Qt.ItemDataRole.UserRole, defn.type)
                cat_item.addChild(node_item)
            cat_item.setExpanded(True)

        if self._library:
            components = self._library.all()
            if components:
                comp_cat = QTreeWidgetItem(["Composants"])
                comp_cat.setFlags(comp_cat.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self._tree.addTopLevelItem(comp_cat)
                for comp in sorted(components, key=lambda c: c.name):
                    item = QTreeWidgetItem([comp.name])
                    item.setData(0, Qt.ItemDataRole.UserRole, f"component:{comp.id}")
                    comp_cat.addChild(item)
                comp_cat.setExpanded(True)

    def _filter(self, text: str) -> None:
        """Show only entries whose label contains *text* (case-insensitive)."""
        query = text.lower()
        for i in range(self._tree.topLevelItemCount()):
            cat_item = self._tree.topLevelItem(i)
            if cat_item is None:
                continue
            visible = 0
            for j in range(cat_item.childCount()):
                child = cat_item.child(j)
                if child is None:
                    continue
                matches = query in child.text(0).lower()
                child.setHidden(not matches)
                if matches:
                    visible += 1
            cat_item.setHidden(visible == 0)

    def _on_double_click(self, item: QTreeWidgetItem, column: int) -> None:
        node_type = item.data(0, Qt.ItemDataRole.UserRole)
        if node_type is not None:
            self.node_type_activated.emit(node_type)
