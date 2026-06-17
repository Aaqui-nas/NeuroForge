from __future__ import annotations

from pytestqt.qtbot import QtBot

from neuroforge.graph.registry import build_default_registry
from neuroforge.ui.palette import NodePalette


class TestNodePalette:
    def test_instantiates(self, qtbot: QtBot) -> None:
        palette = NodePalette(build_default_registry())
        qtbot.addWidget(palette)

    def test_all_categories_shown(self, qtbot: QtBot) -> None:
        registry = build_default_registry()
        palette = NodePalette(registry)
        qtbot.addWidget(palette)
        shown = {
            palette._tree.topLevelItem(i).text(0) for i in range(palette._tree.topLevelItemCount())
        }
        assert shown == set(registry.categories())

    def test_each_category_has_correct_nodes(self, qtbot: QtBot) -> None:
        registry = build_default_registry()
        palette = NodePalette(registry)
        qtbot.addWidget(palette)
        for i in range(palette._tree.topLevelItemCount()):
            cat_item = palette._tree.topLevelItem(i)
            category = cat_item.text(0)
            expected = {d.display_name for d in registry.by_category(category)}
            shown = {cat_item.child(j).text(0) for j in range(cat_item.childCount())}
            assert shown == expected

    def test_all_categories_expanded_by_default(self, qtbot: QtBot) -> None:
        palette = NodePalette(build_default_registry())
        qtbot.addWidget(palette)
        for i in range(palette._tree.topLevelItemCount()):
            assert palette._tree.topLevelItem(i).isExpanded()

    def test_double_click_emits_node_type_activated(self, qtbot: QtBot) -> None:
        registry = build_default_registry()
        palette = NodePalette(registry)
        qtbot.addWidget(palette)
        cat_item = palette._tree.topLevelItem(0)
        leaf = cat_item.child(0)
        with qtbot.waitSignal(palette.node_type_activated, timeout=500) as sig:
            palette._tree.itemDoubleClicked.emit(leaf, 0)
        assert sig.args[0] in [d.type for d in registry.all()]

    def test_double_click_on_category_does_not_emit(self, qtbot: QtBot) -> None:
        palette = NodePalette(build_default_registry())
        qtbot.addWidget(palette)
        received = []
        palette.node_type_activated.connect(received.append)
        cat_item = palette._tree.topLevelItem(0)
        palette._tree.itemDoubleClicked.emit(cat_item, 0)
        assert received == []

    def test_search_shows_matching_nodes(self, qtbot: QtBot) -> None:
        palette = NodePalette(build_default_registry())
        qtbot.addWidget(palette)
        palette._search.setText("linear")
        found = any(
            not palette._tree.topLevelItem(i).child(j).isHidden()
            and "linear" in palette._tree.topLevelItem(i).child(j).text(0).lower()
            for i in range(palette._tree.topLevelItemCount())
            for j in range(palette._tree.topLevelItem(i).childCount())
        )
        assert found

    def test_search_hides_non_matching_nodes(self, qtbot: QtBot) -> None:
        palette = NodePalette(build_default_registry())
        qtbot.addWidget(palette)
        palette._search.setText("xyznonexistent")
        visible = [
            palette._tree.topLevelItem(i).child(j).text(0)
            for i in range(palette._tree.topLevelItemCount())
            for j in range(palette._tree.topLevelItem(i).childCount())
            if not palette._tree.topLevelItem(i).child(j).isHidden()
        ]
        assert visible == []

    def test_search_hides_empty_categories(self, qtbot: QtBot) -> None:
        palette = NodePalette(build_default_registry())
        qtbot.addWidget(palette)
        palette._search.setText("xyznonexistent")
        for i in range(palette._tree.topLevelItemCount()):
            assert palette._tree.topLevelItem(i).isHidden()

    def test_search_is_case_insensitive(self, qtbot: QtBot) -> None:
        palette = NodePalette(build_default_registry())
        qtbot.addWidget(palette)
        palette._search.setText("LINEAR")
        found = any(
            not palette._tree.topLevelItem(i).child(j).isHidden()
            and "linear" in palette._tree.topLevelItem(i).child(j).text(0).lower()
            for i in range(palette._tree.topLevelItemCount())
            for j in range(palette._tree.topLevelItem(i).childCount())
        )
        assert found

    def test_clearing_search_restores_all_nodes(self, qtbot: QtBot) -> None:
        registry = build_default_registry()
        palette = NodePalette(registry)
        qtbot.addWidget(palette)
        palette._search.setText("linear")
        palette._search.setText("")
        visible = [
            palette._tree.topLevelItem(i).child(j).text(0)
            for i in range(palette._tree.topLevelItemCount())
            for j in range(palette._tree.topLevelItem(i).childCount())
            if not palette._tree.topLevelItem(i).child(j).isHidden()
        ]
        assert len(visible) == len(registry.all())
