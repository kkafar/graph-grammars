import networkx as nx
import graphviz
import itertools as it
import matplotlib.pyplot as plt
import argparse
import importlib
from typing import Optional
from dataclasses import dataclass, field
from model import NodeHandle, NodeAttrs, EdgeAttrs, Node, Edge
from graph import Graph
from production import Production, P1, P2, P5, P6

@dataclass
class Args:
    example_name: Optional[str] = None

def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', required=False, type=str,
                        dest='example_name', help='Name of the example to run; if not specified all examples will be run one by one')
    return parser


def run_example(example_name: str):
    if example_name is None:
        example_name = 'example'
    else:
        example_name = 'example.' + example_name

    try:
        module = importlib.import_module(example_name)
        module.main()
    except ImportError:
        print(f"Failed to import module with name {example_name}")
        return


def main():
    args: Args = build_cli().parse_args()
    run_example(args.example_name)


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




if __name__ == '__main__':
    plt.rcParams['figure.figsize'] = (16, 9)
    # test_production()
    # test_production2()
    # monomorphisms()
    # test_production5()
    # test_production6()
    main()
