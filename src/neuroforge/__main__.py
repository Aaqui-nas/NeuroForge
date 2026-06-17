import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from neuroforge.graph.model import DataType, Edge, Graph, Node, Port, PortDirection
from neuroforge.ui.graph_editor.scene import GraphScene
from neuroforge.ui.graph_editor.view import GraphView


def make_port(pid: str, direction: PortDirection) -> Port:
    return Port(
        id=pid,
        name=pid,
        direction=direction,
        data_type=DataType.TENSOR,
        required=True,
    )


g = Graph()

n1 = Node(
    id="a",
    type="input",
    name="Input",
    position=(50, 100),
    ports={"output": make_port("output", PortDirection.OUTPUT)},
    params={},
)

n2 = Node(
    id="b",
    type="linear",
    name="Linear",
    position=(300, 80),
    ports={
        "input": make_port("input", PortDirection.INPUT),
        "output": make_port("output", PortDirection.OUTPUT),
    },
    params={},
)

n3 = Node(
    id="c",
    type="relu",
    name="ReLU",
    position=(550, 80),
    ports={
        "input": make_port("input", PortDirection.INPUT),
        "output": make_port("output", PortDirection.OUTPUT),
    },
    params={},
)

n4 = Node(
    id="d",
    type="output",
    name="Output",
    position=(800, 100),
    ports={"input": make_port("input", PortDirection.INPUT)},
    params={},
)

for n in (n1, n2, n3, n4):
    g.add_node(n)

g.add_edge(Edge(id="e1", src_node="a", src_port="output", dst_node="b", dst_port="input"))
g.add_edge(Edge(id="e2", src_node="b", src_port="output", dst_node="c", dst_port="input"))
g.add_edge(Edge(id="e3", src_node="c", src_port="output", dst_node="d", dst_port="input"))

app = QApplication(sys.argv)

win = QMainWindow()
win.resize(1280, 720)
win.setWindowTitle("NeuroForge — test UI")

scene = GraphScene(g)
view = GraphView(scene)

win.setCentralWidget(view)
win.show()

sys.exit(app.exec())
