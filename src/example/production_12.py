import matplotlib.pyplot as plt
import itertools as it
from graph import Graph
from model import Node, NodeAttrs, Edge, EdgeAttrs
from production import P12


def main():
    fig, plots = plt.subplots(nrows=1, ncols=2)
    graph = Graph()

    node_0 = Node(NodeAttrs('v', 0, 0, False))
    node_1 = Node(NodeAttrs('v', 1, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 1, False))
    node_3 = Node(NodeAttrs('v', 0, 1, False))
    node_4 = Node(NodeAttrs('v', 1.83, 0.5, False))
    node_5 = Node(NodeAttrs('v', 0.5, 0, True))
    node_6 = Node(NodeAttrs('v', 0.5, 1, True))
    nodes = [node_0, node_5, node_1, node_4, node_2, node_6, node_3]
    corner_nodes = (node_0, node_1, node_2, node_3, node_4)

    graph.add_node_collection(nodes)

    graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

    for node_a, node_b in it.pairwise(nodes + [node_0]):
        graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

    graph.display(ax=plots[0])
    plots[0].set(title='Before')

    assert P12()(graph)

    graph.display(ax=plots[1])
    plots[1].set(title='After')

    fig.suptitle("Applying production 12")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
