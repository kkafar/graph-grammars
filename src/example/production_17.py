import matplotlib.pyplot as plt
import itertools as it
from graph import Graph
from model import Node, NodeAttrs, Edge, EdgeAttrs
from production import P17


def main():
    fig, plots = plt.subplots(nrows=1, ncols=2)
    graph = Graph()

    node_1 = Node(NodeAttrs('v', 0, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 0, False))
    node_3 = Node(NodeAttrs('v', 1, 1, False))
    node_4 = Node(NodeAttrs('v', 0, 1, False))
    node_5 = Node(NodeAttrs('v', 1, 0.5, True))
    node_6 = Node(NodeAttrs('v', 2, 0.5, False))
    node_7 = Node(NodeAttrs('v', 2, 1, False))
    node_8 = Node(NodeAttrs('v', 0.5, 0, False))

    nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]

    graph.add_node_collection(nodes)

    graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False))
    graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', True))

    graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
    graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))


    graph.display(ax=plots[0])
    plots[0].set(title='Before')

    assert P17()(graph)

    graph.display(ax=plots[1])
    plots[1].set(title='After')

    fig.suptitle("Applying production 17")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
