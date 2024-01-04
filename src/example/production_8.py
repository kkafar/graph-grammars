import matplotlib.pyplot as plt
import itertools as it
from graph import Graph
from model import Node, NodeAttrs, Edge, EdgeAttrs
from production import P8


def main():
    fig, plots = plt.subplots(nrows=1, ncols=2)
    graph = Graph()

    node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
    node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
    node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
    node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
    node_4 = Node(NodeAttrs('v', 1, 0.5, True), 4)
    node_5 = Node(NodeAttrs('v', 2, 0.5, False), 5)
    node_6 = Node(NodeAttrs('v', 2, 1, False), 6)
    nodes = [node_0, node_1, node_4, node_2, node_3, node_5, node_6]
    corner_nodes1 = (node_0, node_1, node_2, node_3)
    corner_nodes2 = (node_4, node_5, node_6, node_2)

    graph.add_node_collection(nodes)

    graph.add_q_hyperedge(corner_nodes1, EdgeAttrs('q', False), 7)
    graph.add_q_hyperedge(corner_nodes2, EdgeAttrs('q', True), 8)

    graph.add_edge(Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
    graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

    graph.display(ax=plots[0])
    plots[0].set(title='Before')

    assert P8()(graph)

    graph.display(ax=plots[1])
    plots[1].set(title='After')

    fig.suptitle("Applying production 8")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
