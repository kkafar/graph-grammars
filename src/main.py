import networkx as nx
import graphviz
import itertools as it
import matplotlib.pyplot as plt
from model import NodeHandle, NodeAttrs, EdgeAttrs, Node, Edge
from graph import Graph
from production import Production, P1

def main():
    graph = Graph()

    node_1 = Node(NodeAttrs('v', 0, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 0, False))
    node_3 = Node(NodeAttrs('v', 1, 1, False))
    node_4 = Node(NodeAttrs('v', 0, 1, False))
    nodes = [ node_1, node_2, node_3, node_4 ]

    graph.add_node_collection(nodes)

    for node_1, node_2 in it.pairwise(nodes + [node_1]):
        graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', value=False)))

    print(graph.nx_graph.nodes)
    print(graph.nx_graph.edges)

    subgraph = Graph()
    subgraph.add_node_collection(nodes[:2])
    for node_1, node_2 in it.pairwise(nodes[:2]):
        subgraph.add_edge(Edge(node_1.handle, node_2.handle, None))

    print('Mapping')
    for mapping in graph.generate_subgraphs_isomorphic_with(subgraph):
        print(mapping)

    fig, plots = plt.subplots(nrows=1, ncols=2)
    graph.display(ax=plots[0])
    subgraph.display(ax=plots[1])

    fig.savefig('graphs.png')
    fig.tight_layout()
    plt.show()


def test_production():
    graph = Graph()

    node_1 = Node(NodeAttrs('v', 0, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 0, False))
    node_3 = Node(NodeAttrs('v', 1, 1, False))
    node_4 = Node(NodeAttrs('v', 0, 1, False))
    nodes = [ node_1, node_2, node_3, node_4 ]

    graph.add_node_collection(nodes)

    for node_1, node_2 in it.pairwise(nodes + [node_1]):
        graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', value=False)))

    P1()(graph)
    P1()(graph)
    # p1_instance = P1()


if __name__ == '__main__':
    plt.rcParams['figure.figsize'] = (16, 9)
    test_production()
    # main()
