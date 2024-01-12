from graph import Graph
from production import (
    Production,
    P9, P8, P16, P7, P2, P1, P3
)
from model import Node, NodeAttrs, Edge, EdgeAttrs
from driver import Driver, UserInput
import itertools as it
import matplotlib.pyplot as plt
import basic_graph as gu


def create_graph() -> Graph:
    graph = Graph()

    inner_nodes = [
        Node(NodeAttrs('v', 0, 0, False)),
        Node(NodeAttrs('v', 1, 0, False)),
        Node(NodeAttrs('v', 1.5, 0.5, False)),
        Node(NodeAttrs('v', 1, 1, False)),
        Node(NodeAttrs('v', 0, 1, False)),
    ]

    outer_nodes = [
        Node(NodeAttrs('v', -1, -1, False)),
        Node(NodeAttrs('v', 2, -1, False)),
        Node(NodeAttrs('v', 2, 0.5, False)),
        Node(NodeAttrs('v', 2, 2, False)),
        Node(NodeAttrs('v', -1, 2, False)),
    ]

    graph.add_node_collection(inner_nodes)
    graph.add_node_collection(outer_nodes)

    for node_u, node_v in it.pairwise(inner_nodes + [inner_nodes[0]]):
        graph.add_edge(Edge(node_u.handle, node_v.handle, EdgeAttrs('e', False)))

    for node_u, node_v in it.pairwise(outer_nodes + [outer_nodes[0]]):
        graph.add_edge(Edge(node_u.handle, node_v.handle, EdgeAttrs('e', True)))

    graph.add_p_hyperedge(inner_nodes, EdgeAttrs('p', False))

    for node_u, node_v in zip(inner_nodes, outer_nodes):
        graph.add_edge(Edge(node_u.handle, node_v.handle, EdgeAttrs('e', False)))


    for (node_a, node_b), (node_c, node_d) in zip(it.pairwise(inner_nodes + [inner_nodes[0]]), it.pairwise(outer_nodes + [outer_nodes[0]])):
        graph.add_q_hyperedge((node_a, node_b, node_c, node_d), EdgeAttrs('q', False))

    return graph


def main():
    graph = create_graph()
    driver = Driver()

    driver.execute_production_sequence(graph, [P16(), P9(), UserInput(23), P8(), P8(), P2(), P3(), P1(), UserInput(46), P8(), P8(), P2(), P3(), P1()])

    graph.display()


    plt.show()
