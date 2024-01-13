from graph import Graph
from production import (
    Production,
    P9, P8, P16, P7, P2, P1, P3, P17, P11
)
from model import Node, NodeAttrs, Edge, EdgeAttrs
from driver import Driver, FixedInput, DrawingDriverDelegate
from pathlib import Path
import itertools as it
import matplotlib.pyplot as plt
import basic_graph as gu


def create_graph() -> Graph:
    G = Graph()
    
    node_0 = Node(NodeAttrs('v', -1, 0, False))
    node_1 = Node(NodeAttrs('v', 2, 0, False))
    node_2 = Node(NodeAttrs('v', 3, -1.5, False))
    node_3 = Node(NodeAttrs('v', 2, -3, False))
    node_4 = Node(NodeAttrs('v', -1, -3, False))
    node_5 = Node(NodeAttrs('v', -2, 2, False))
    node_6 = Node(NodeAttrs('v', 5, 2, False))

    node_7 = Node(NodeAttrs('v', 5, -1.5, False)) # outer

    node_8 = Node(NodeAttrs('v', 5, -5, False))
    node_9 = Node(NodeAttrs('v', -2, -5, False))

    nodes = [node_0, node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9]
    G.add_node_collection(nodes)
    
    edges = [
        Edge(node_0.handle, node_1.handle, EdgeAttrs('e', False)),
        Edge(node_1.handle, node_2.handle, EdgeAttrs('e', False)),
        Edge(node_2.handle, node_3.handle, EdgeAttrs('e', False)),
        Edge(node_3.handle, node_4.handle, EdgeAttrs('e', False)),
        Edge(node_4.handle, node_0.handle, EdgeAttrs('e', False)),
        Edge(node_0.handle, node_5.handle, EdgeAttrs('e', False)),
        Edge(node_1.handle, node_6.handle, EdgeAttrs('e', False)),
        Edge(node_2.handle, node_7.handle, EdgeAttrs('e', False)),
        Edge(node_3.handle, node_8.handle, EdgeAttrs('e', False)),
        Edge(node_4.handle, node_9.handle, EdgeAttrs('e', False)),
        Edge(node_5.handle, node_6.handle, EdgeAttrs('e', True)),
        Edge(node_6.handle, node_7.handle, EdgeAttrs('e', True)),
        Edge(node_7.handle, node_8.handle, EdgeAttrs('e', True)),
        Edge(node_8.handle, node_9.handle, EdgeAttrs('e', True)),
        Edge(node_9.handle, node_5.handle, EdgeAttrs('e', True))
    ]

    G.add_edge_collection(edges)

    G.add_q_hyperedge((node_0, node_1, node_6, node_5), EdgeAttrs('q', False))
    G.add_q_hyperedge((node_1, node_2, node_7, node_6), EdgeAttrs('q', False))
    G.add_q_hyperedge((node_2, node_3, node_8, node_7), EdgeAttrs('q', False))
    G.add_q_hyperedge((node_3, node_4, node_9, node_8), EdgeAttrs('q', False))
    G.add_q_hyperedge((node_0, node_4, node_9, node_5), EdgeAttrs('q', False))
    G.add_p_hyperedge((node_0, node_1, node_2, node_3, node_4), EdgeAttrs('p', False))

    return G


class AxesProvider:
    def __iter__(self):
        return self

    def __next__(self):
        _fig, axes = plt.subplots(nrows=1, ncols=1)
        return axes

def main():
    savedir = Path('docs/derivation_1/')
    if not savedir.is_dir():
        savedir.mkdir(parents=True)

    graph = create_graph()

    driver = Driver()
    driver.delegate = DrawingDriverDelegate(savedir)

    driver.execute_production_sequence(graph, [
        FixedInput(11),
        P1(),
        FixedInput(21),
        P8(),
        P17(),
        P2(),
        P11(),
        P1(),
        FixedInput(47),
        P8(),
        P8(),
        P2(),
        P3(),
        P1()
    ])

    graph.display()
    plt.savefig("control.png")