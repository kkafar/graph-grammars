import networkx as nx
import graphviz
import itertools as it
import matplotlib.pyplot as plt
import util
import sys
from model import NodeHandle, NodeAttrs, EdgeAttrs, Node, Edge
from graph import Graph
from prods.p1 import P1
from prods.p2 import P2
from prods.p9 import P9
from prods.p10 import P10
from prods.p16 import P16
#from prods import Production, P1, P2, P9, P10, P16

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
    nodes = [node_1, node_2, node_3, node_4]

    graph.add_node_collection(nodes)

    # Add two edges of type Q, note that they have the same handle!!!
    q_edge = Edge(node_1.handle, node_3.handle, EdgeAttrs(kind='q', value=True))
    q_edge_2 = Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='q', value=True, handle=q_edge.attrs.handle))
    graph.add_edge(q_edge)
    graph.add_edge(q_edge_2)

    for node_1, node_2 in it.pairwise(nodes + [node_1]):
        graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', value=False)))

    P1()(graph)
    # p1_instance = P1()


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
    q_edge = Edge(node_0.handle, node_2.handle, EdgeAttrs(kind='q', value=True))
    q_edge_2 = Edge(node_1.handle, node_3.handle, EdgeAttrs(kind='q', value=True, handle=q_edge.attrs.handle))
    graph.add_edge(q_edge)
    graph.add_edge(q_edge_2)

    for node_1, node_2 in it.pairwise(nodes + [node_0]):
        graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', value=False)))

    # graph.display()
    # plt.show()

    P2()(graph)

def test_16():

    graph, _ = util.basic_star5()
    graph.display()
    plt.show()
    P16(5)(graph)

def test_16_9():

    graph = util.basic_pentagon()
    graph.display()
    plt.show()
    P16()(graph)
    P9()(graph)

def test_10():

    graph = util.basic_pentagon()
    graph.add_hanging_node(u=0, v=1)

    graph.display()
    plt.show()

    P16()(graph)

    P10()(graph)

    P1()(graph)

def test_1():
    graph = util.basic_square()

    # example to show why we use monomorphism instead
    # of isomorphism:
    #attr = EdgeAttrs('e', False)
    #edge = Edge(2, 0, attr)
    #graph.add_edge(edge)

    graph.display()
    plt.show()

    P1()(graph)

if __name__ == '__main__':
    plt.rcParams['figure.figsize'] = (16, 9)
    if len(sys.argv) < 2:
        print("please provide one of the arguments: 1, 16, 169, 10")
        exit()
    arg = sys.argv[1]
    if arg == '1':
        test_1()
    elif arg == '16':
        test_16()
    elif arg == '169':
        test_16_9()
    elif arg == '10':
        test_10()
