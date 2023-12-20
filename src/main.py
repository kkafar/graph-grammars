import networkx as nx
import graphviz
import itertools as it
import matplotlib.pyplot as plt
from model import NodeHandle, NodeAttrs, EdgeAttrs, Node, Edge
from graph import Graph
from production import Production, P1, P2, P5, P6, P11, P12, P17

def main():
    graph = Graph()

    node_1 = Node(NodeAttrs('v', 0, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 0, False))
    node_3 = Node(NodeAttrs('v', 1, 1, False))
    node_4 = Node(NodeAttrs('v', 0, 1, False))
    nodes = [ node_1, node_2, node_3, node_4 ]

    graph.add_node_collection(nodes)

    for node_1, node_2 in it.pairwise(nodes + [node_1]):
        graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

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
    nodes = [node_1, node_2, node_3, node_4]

    graph.add_node_collection(nodes)

    # Add two edges of type Q, note that they have the same handle!!!
    graph.add_q_hyperedge(nodes, EdgeAttrs('q', True))

    for node_1, node_2 in it.pairwise(nodes + [node_1]):
        graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

    graph.display()
    plt.show()

    assert P1()(graph)


def test_production2():
    graph = Graph()

    node_0 = Node(NodeAttrs('v', 0, 0, False))
    node_1 = Node(NodeAttrs('v', 1, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 1, False))
    node_3 = Node(NodeAttrs('v', 0, 1, False))
    node_4 = Node(NodeAttrs('v', 1, 0.5, True))
    nodes = [node_0, node_1, node_4, node_2, node_3]

    graph.add_node_collection(nodes)

    # Add two edges of type Q, note that they have the same handle!!!
    graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', True))

    for node_1, node_2 in it.pairwise(nodes + [node_0]):
        graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

    graph.display()
    plt.show()

    assert P2()(graph)

def test_production5():
    graph = Graph()

    node_0 = Node(NodeAttrs('v', 0, 0, False))
    node_1 = Node(NodeAttrs('v', 1, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 1, False))
    node_3 = Node(NodeAttrs('v', 0, 1, False))
    node_4 = Node(NodeAttrs('v', 1, 0.5, True))
    node_5 = Node(NodeAttrs('v', 0, 0.5, True))
    node_6 = Node(NodeAttrs('v', 0.5, 0, True))
    nodes = [node_0, node_6, node_1, node_4, node_2, node_3, node_5]
    graph.add_node_collection(nodes)

    # Add two edges of type Q, note that they have the same handle!!!
    graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', True))

    for node_1, node_2 in it.pairwise(nodes + [node_0]):
        graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

    graph.display()
    plt.show()

    P5()(graph)

def test_production6():
    graph = Graph()

    node_0 = Node(NodeAttrs('v', 0, 0, False))
    node_1 = Node(NodeAttrs('v', 1, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 1, False))
    node_3 = Node(NodeAttrs('v', 0, 1, False))
    node_4 = Node(NodeAttrs('v', 1, 0.5, True))
    node_5 = Node(NodeAttrs('v', 0.5, 1, True))
    node_6 = Node(NodeAttrs('v', 0, 0.5, True))
    node_7 = Node(NodeAttrs('v', 0.5, 0, True))
    nodes = [node_0, node_7, node_1, node_4, node_2, node_5, node_3, node_6]
    graph.add_node_collection(nodes)

    # Add two edges of type Q, note that they have the same handle!!!
    graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', True))

    for node_1, node_2 in it.pairwise(nodes + [node_0]):
        graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

    graph.display()
    plt.show()

    P6()(graph)


def monomorphisms():
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
    plt.show()


    monomorphic_mappings = list(graph.generate_subgraphs_monomorphic_with(subgraph))
    isomorphic_mappings = list(graph.generate_subgraphs_isomorphic_with(subgraph))

    print(f"Isomorphic count: {len(isomorphic_mappings)}, Monomorhpic count: {len(monomorphic_mappings)}")


def test_production11():
    graph = Graph()

    node_0 = Node(NodeAttrs('v', 0, 0, False))
    node_1 = Node(NodeAttrs('v', 1, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 1, False))
    node_3 = Node(NodeAttrs('v', 0, 1, False))
    node_4 = Node(NodeAttrs('v', 1.83, 0.5, False))
    node_5 = Node(NodeAttrs('v', 0.5, 0, True))
    node_6 = Node(NodeAttrs('v', 0, 0.5, True))
    nodes = [node_0, node_5, node_1, node_4, node_2, node_3, node_6]
    corner_nodes = (node_0, node_1, node_2, node_3, node_4)

    graph.add_node_collection(nodes)

    graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

    for node_a, node_b in it.pairwise(nodes + [node_0]):
        graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

    # graph.display()
    # plt.savefig("graph11_basic.png")
    # plt.show()

    P11()(graph)

    graph.display()
    plt.savefig("graph11_modified.png")

def test_production11_complex():
    graph = Graph()

    node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
    node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
    node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
    node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
    node_4 = Node(NodeAttrs('v', 1.83, 0.5, False), 4)
    node_5 = Node(NodeAttrs('v', 0.5, 0, True), 5)
    node_6 = Node(NodeAttrs('v', 0, 0.5, True), 6)

    node_8 = Node(NodeAttrs('v', 1, 2, True), 8)
    node_9 = Node(NodeAttrs('v', 0, 2, True), 9)
    nodes = [node_0, node_5, node_1, node_4, node_2, node_3, node_6, node_8, node_9]
    corner_nodes = (node_0, node_1, node_2, node_3, node_4)

    graph.add_node_collection(nodes)

    graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True), 7)

    for node_a, node_b in it.pairwise(nodes[:-2] + [node_0]):
        graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))
    
    graph.add_edge(Edge(node_2.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
    graph.add_edge(Edge(node_8.handle, node_9.handle, EdgeAttrs(kind='e', flag=False)))
    graph.add_edge(Edge(node_9.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

    graph.add_q_hyperedge((node_2, node_8, node_9, node_3), EdgeAttrs('q', False))

    # graph.display()
    # plt.savefig("graph11_complex.png")

    P11()(graph)

    graph.display()
    plt.savefig("graph11_complex_modified.png")


def test_production12():
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

    P12()(graph)

    graph.display()
    plt.savefig("graph12_modified.png")


def test_production12_complex():
    graph = Graph()

    node_8 = Node(NodeAttrs('v', -1, 0, True), 8)
    node_9 = Node(NodeAttrs('v', -1, 1, True), 9)

    node_0 = Node(NodeAttrs('v', 0, 0, False))
    node_1 = Node(NodeAttrs('v', 1, 0, False))
    node_2 = Node(NodeAttrs('v', 1, 1, False))
    node_3 = Node(NodeAttrs('v', 0, 1, False))
    node_4 = Node(NodeAttrs('v', 1.83, 0.5, False))
    node_5 = Node(NodeAttrs('v', 0.5, 0, True))
    node_6 = Node(NodeAttrs('v', 0.5, 1, True))
    nodes = [node_0, node_5, node_1, node_4, node_2, node_6, node_3, node_8, node_9]
    corner_nodes = (node_0, node_1, node_2, node_3, node_4)

    graph.add_node_collection(nodes)

    graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True), 7)

    for node_a, node_b in it.pairwise(nodes[:-2] + [node_0]):
        if node_a.handle + node_b.handle == 6 and node_a.handle * node_b.handle == 0:
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))
        else:
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))
    
    graph.add_edge(Edge(node_0.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
    graph.add_edge(Edge(node_8.handle, node_9.handle, EdgeAttrs(kind='e', flag=False)))
    graph.add_edge(Edge(node_9.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

    graph.add_q_hyperedge((node_3, node_8, node_9, node_0), EdgeAttrs('q', False))

    # graph.display()
    # plt.savefig("graph12_complex.png")

    P12()(graph)

    graph.display()
    plt.savefig("graph12_complex_modified.png")


def test_production17():
    graph = Graph()

    node_1 = Node(NodeAttrs('v', 0, 0, False), 1)
    node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
    node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
    node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
    node_5 = Node(NodeAttrs('v', 1, 0.5, True), 5)
    node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
    node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
    node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

    nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]

    graph.add_node_collection(nodes)

    graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False), 9)
    graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', True))

    graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
    graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

    # graph.display()
    # plt.savefig("graph17_basic.png")

    P17()(graph)

    graph.display()
    plt.savefig("graph17_modified.png")


if __name__ == '__main__':
    plt.rcParams['figure.figsize'] = (16, 9)
    # test_production()
    # test_production2()
    # test_production5()
    # test_production6()
    # test_production11()
    test_production11_complex()
    # test_production12()
    # test_production12_complex()
    # test_production17()
    # main()
