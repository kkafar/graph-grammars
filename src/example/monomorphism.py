import matplotlib.pyplot as plt
import itertools as it
from graph import Graph
from model import Node, NodeAttrs, Edge, EdgeAttrs
from production.production_1 import P1


def main():
    fig, plots = plt.subplots(nrows=1, ncols=2)

    graph = Graph()
    node_0 = Node(NodeAttrs('v', 0, 0, False))
    node_1 = Node(NodeAttrs('v', 1, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 1, False))
    node_3 = Node(NodeAttrs('v', 0, 1, False))
    nodes = [node_0, node_1, node_2, node_3]
    graph.add_node_collection(nodes)

    graph.add_q_hyperedge(nodes, EdgeAttrs('q', True))

    for node_a, node_b in it.pairwise(nodes + [node_0]):
        graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

    graph.display(ax=plots[0])


    subgraph = Graph()
    node_0 = Node(NodeAttrs('v', 0, 0, False))
    node_1 = Node(NodeAttrs('v', 1, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 1, False))
    node_3 = Node(NodeAttrs('v', 0, 1, False))
    sg_nodes = [node_0, node_1, node_2, node_3]
    subgraph.add_node_collection(sg_nodes)
    subgraph.add_q_hyperedge(sg_nodes, EdgeAttrs('q', True))

    subgraph.display(ax=plots[1])

    plots[0].set(title='Graph')
    plots[1].set(title='Subgraph')
    fig.suptitle('Monomorphic subgraph detection')

    plt.show()

    monomorphic_mappings = list(graph.generate_subgraphs_monomorphic_with(subgraph))
    isomorphic_mappings = list(graph.generate_subgraphs_isomorphic_with(subgraph))

    print(f"Isomorphic count: {len(isomorphic_mappings)}, Monomorhpic count: {len(monomorphic_mappings)}")


if __name__ == "__main__":
    main()

