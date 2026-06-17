from __future__ import annotations

from neuroforge.graph.commands import (
    AddEdgeCommand,
    AddNodeCommand,
    Command,
    CommandHistory,
    GroupNodesCommand,
    MacroCommand,
    MoveNodeCommand,
    RemoveEdgeCommand,
    RemoveNodeCommand,
    UpdateParamCommand,
)
from neuroforge.graph.model import Edge, Graph, Node

# ── Helpers ───────────────────────────────────────────────────────────────────


def make_node(nid: str, pos: tuple[float, float] = (0.0, 0.0)) -> Node:
    return Node(id=nid, type="linear", name=nid, position=pos, ports={}, params={})


def make_edge(eid: str, src: str, dst: str) -> Edge:
    return Edge(id=eid, src_node=src, src_port="out", dst_node=dst, dst_port="in")


def two_node_graph() -> Graph:
    g = Graph()
    g.add_node(make_node("a"))
    g.add_node(make_node("b"))
    g.add_edge(make_edge("e1", "a", "b"))
    return g


class _TrackingCommand(Command):
    """Minimal command that records execute/undo call counts."""

    def __init__(self) -> None:
        self.execute_count = 0
        self.undo_count = 0

    def execute(self) -> None:
        self.execute_count += 1

    def undo(self) -> None:
        self.undo_count += 1


# ── CommandHistory ────────────────────────────────────────────────────────────


class TestCommandHistory:
    def test_push_executes_command(self) -> None:
        h = CommandHistory()
        cmd = _TrackingCommand()
        h.push(cmd)
        assert cmd.execute_count == 1

    def test_push_enables_undo(self) -> None:
        h = CommandHistory()
        h.push(_TrackingCommand())
        assert h.can_undo()

    def test_initial_state_cannot_undo(self) -> None:
        assert not CommandHistory().can_undo()

    def test_initial_state_cannot_redo(self) -> None:
        assert not CommandHistory().can_redo()

    def test_undo_calls_command_undo(self) -> None:
        h = CommandHistory()
        cmd = _TrackingCommand()
        h.push(cmd)
        h.undo()
        assert cmd.undo_count == 1

    def test_undo_disables_undo_when_empty(self) -> None:
        h = CommandHistory()
        h.push(_TrackingCommand())
        h.undo()
        assert not h.can_undo()

    def test_undo_enables_redo(self) -> None:
        h = CommandHistory()
        h.push(_TrackingCommand())
        h.undo()
        assert h.can_redo()

    def test_redo_re_executes_command(self) -> None:
        h = CommandHistory()
        cmd = _TrackingCommand()
        h.push(cmd)
        h.undo()
        h.redo()
        assert cmd.execute_count == 2

    def test_redo_disables_redo_when_at_end(self) -> None:
        h = CommandHistory()
        h.push(_TrackingCommand())
        h.undo()
        h.redo()
        assert not h.can_redo()

    def test_push_after_undo_discards_redo_branch(self) -> None:
        h = CommandHistory()
        cmd_a = _TrackingCommand()
        cmd_b = _TrackingCommand()
        cmd_c = _TrackingCommand()
        h.push(cmd_a)
        h.push(cmd_b)
        h.undo()
        h.push(cmd_c)
        assert not h.can_redo()

    def test_undo_no_op_when_nothing_to_undo(self) -> None:
        h = CommandHistory()
        h.undo()  # must not raise

    def test_redo_no_op_when_nothing_to_redo(self) -> None:
        h = CommandHistory()
        h.redo()  # must not raise

    def test_clear_empties_history(self) -> None:
        h = CommandHistory()
        h.push(_TrackingCommand())
        h.push(_TrackingCommand())
        h.clear()
        assert not h.can_undo()
        assert not h.can_redo()

    def test_max_size_trims_oldest_command(self) -> None:
        h = CommandHistory()
        cmds = [_TrackingCommand() for _ in range(CommandHistory.MAX_SIZE + 5)]
        for cmd in cmds:
            h.push(cmd)
        # Should be able to undo exactly MAX_SIZE times
        undo_count = 0
        while h.can_undo():
            h.undo()
            undo_count += 1
        assert undo_count == CommandHistory.MAX_SIZE


# ── MacroCommand ──────────────────────────────────────────────────────────────


class TestMacroCommand:
    def test_execute_calls_all_sub_commands(self) -> None:
        cmds = [_TrackingCommand() for _ in range(3)]
        MacroCommand(cmds).execute()
        assert all(c.execute_count == 1 for c in cmds)

    def test_undo_calls_all_sub_commands_in_reverse(self) -> None:
        order: list[int] = []

        class _OrderCmd(Command):
            def __init__(self, idx: int) -> None:
                self._idx = idx

            def execute(self) -> None:
                pass

            def undo(self) -> None:
                order.append(self._idx)

        cmds = [_OrderCmd(i) for i in range(3)]
        macro = MacroCommand(cmds)
        macro.execute()
        macro.undo()
        assert order == [2, 1, 0]


# ── AddNodeCommand ────────────────────────────────────────────────────────────


class TestAddNodeCommand:
    def test_execute_adds_node(self) -> None:
        g = Graph()
        node = make_node("n1")
        AddNodeCommand(g, node).execute()
        assert "n1" in g.nodes

    def test_undo_removes_node(self) -> None:
        g = Graph()
        node = make_node("n1")
        cmd = AddNodeCommand(g, node)
        cmd.execute()
        cmd.undo()
        assert "n1" not in g.nodes


# ── RemoveNodeCommand ─────────────────────────────────────────────────────────


class TestRemoveNodeCommand:
    def test_execute_removes_node(self) -> None:
        g = two_node_graph()
        RemoveNodeCommand(g, "a").execute()
        assert "a" not in g.nodes

    def test_undo_restores_node(self) -> None:
        g = two_node_graph()
        cmd = RemoveNodeCommand(g, "a")
        cmd.execute()
        cmd.undo()
        assert "a" in g.nodes

    def test_execute_removes_connected_edges(self) -> None:
        g = two_node_graph()
        RemoveNodeCommand(g, "a").execute()
        assert "e1" not in g.edges

    def test_undo_restores_connected_edges(self) -> None:
        g = two_node_graph()
        cmd = RemoveNodeCommand(g, "a")
        cmd.execute()
        cmd.undo()
        assert "e1" in g.edges

    def test_execute_on_missing_node_is_safe(self) -> None:
        g = Graph()
        RemoveNodeCommand(g, "nonexistent").execute()  # must not raise


# ── MoveNodeCommand ───────────────────────────────────────────────────────────


class TestMoveNodeCommand:
    def test_execute_moves_node(self) -> None:
        g = Graph()
        g.add_node(make_node("n1", (0.0, 0.0)))
        MoveNodeCommand(g, "n1", (0.0, 0.0), (100.0, 200.0)).execute()
        assert g.nodes["n1"].position == (100.0, 200.0)

    def test_undo_restores_position(self) -> None:
        g = Graph()
        g.add_node(make_node("n1", (0.0, 0.0)))
        cmd = MoveNodeCommand(g, "n1", (0.0, 0.0), (100.0, 200.0))
        cmd.execute()
        cmd.undo()
        assert g.nodes["n1"].position == (0.0, 0.0)


# ── AddEdgeCommand ────────────────────────────────────────────────────────────


class TestAddEdgeCommand:
    def test_execute_adds_edge(self) -> None:
        g = Graph()
        g.add_node(make_node("a"))
        g.add_node(make_node("b"))
        edge = make_edge("e1", "a", "b")
        AddEdgeCommand(g, edge).execute()
        assert "e1" in g.edges

    def test_undo_removes_edge(self) -> None:
        g = Graph()
        g.add_node(make_node("a"))
        g.add_node(make_node("b"))
        edge = make_edge("e1", "a", "b")
        cmd = AddEdgeCommand(g, edge)
        cmd.execute()
        cmd.undo()
        assert "e1" not in g.edges


# ── RemoveEdgeCommand ─────────────────────────────────────────────────────────


class TestRemoveEdgeCommand:
    def test_execute_removes_edge(self) -> None:
        g = two_node_graph()
        RemoveEdgeCommand(g, "e1").execute()
        assert "e1" not in g.edges

    def test_undo_restores_edge(self) -> None:
        g = two_node_graph()
        cmd = RemoveEdgeCommand(g, "e1")
        cmd.execute()
        cmd.undo()
        assert "e1" in g.edges

    def test_execute_on_missing_edge_is_safe(self) -> None:
        g = Graph()
        RemoveEdgeCommand(g, "nonexistent").execute()  # must not raise


# ── UpdateParamCommand ────────────────────────────────────────────────────────


class TestUpdateParamCommand:
    def test_execute_sets_param(self) -> None:
        g = Graph()
        g.add_node(make_node("n1"))
        UpdateParamCommand(g, "n1", "lr", None, 0.01).execute()
        assert g.nodes["n1"].params["lr"] == 0.01

    def test_undo_restores_old_value(self) -> None:
        g = Graph()
        g.add_node(make_node("n1"))
        g.nodes["n1"].params["lr"] = 0.001
        cmd = UpdateParamCommand(g, "n1", "lr", 0.001, 0.01)
        cmd.execute()
        cmd.undo()
        assert g.nodes["n1"].params["lr"] == 0.001

    def test_undo_removes_param_when_old_value_was_none(self) -> None:
        g = Graph()
        g.add_node(make_node("n1"))
        cmd = UpdateParamCommand(g, "n1", "lr", None, 0.01)
        cmd.execute()
        cmd.undo()
        assert "lr" not in g.nodes["n1"].params


# ── GroupNodesCommand ─────────────────────────────────────────────────────────


class TestGroupNodesCommand:
    def test_execute_removes_selected_nodes(self) -> None:
        g = two_node_graph()
        GroupNodesCommand(g, ["a", "b"], "MyGroup").execute()
        assert "a" not in g.nodes
        assert "b" not in g.nodes

    def test_undo_restores_nodes(self) -> None:
        g = two_node_graph()
        cmd = GroupNodesCommand(g, ["a", "b"], "MyGroup")
        cmd.execute()
        cmd.undo()
        assert "a" in g.nodes
        assert "b" in g.nodes

    def test_execute_removes_internal_edges(self) -> None:
        g = two_node_graph()
        GroupNodesCommand(g, ["a", "b"], "MyGroup").execute()
        assert "e1" not in g.edges

    def test_undo_restores_internal_edges(self) -> None:
        g = two_node_graph()
        cmd = GroupNodesCommand(g, ["a", "b"], "MyGroup")
        cmd.execute()
        cmd.undo()
        assert "e1" in g.edges
