import basic_graph
import matplotlib.pyplot as plt
from production import P7
from model import Node, NodeAttrs, Edge, EdgeAttrs
from graph import Graph
import itertools as it

def main():
    fig, plots = plt.subplots(nrows=1, ncols=2)

    graph = Graph()

    node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
    node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
    node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
    node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
    nodes = [node_0, node_1, node_2, node_3]
    graph.add_node_collection(nodes)
    graph.add_q_hyperedge(nodes, EdgeAttrs('q', False), 4)

    graph.display(ax=plots[0])
    plots[0].set(title='Before')

    assert P7()(graph)

    graph.display(ax=plots[1])
    plots[1].set(title='After')

    fig.suptitle("Applying production 7")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

