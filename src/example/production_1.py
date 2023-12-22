import matplotlib.pyplot as plt
import itertools as it
from graph import Graph
from model import Node, NodeAttrs, Edge, EdgeAttrs
from production.production_1 import P1

def main():
    graph = Graph()

    node_1 = Node(NodeAttrs('v', 0, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 0, False))
    node_3 = Node(NodeAttrs('v', 1, 1, False))
    node_4 = Node(NodeAttrs('v', 0, 1, False))
    nodes = [node_1, node_2, node_3, node_4]

    graph.add_node_collection(nodes)

    # Add two edges of type Q, note that they have the same handle!!!
    graph.add_q_hyperedge(nodes, EdgeAttrs('q', True))

    for node_1, node_2 in it.pairwise(nodes + [node_1]):
        graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

    graph.display()
    plt.show()

    assert P1()(graph)


if __name__ == "__main__":
    main()
