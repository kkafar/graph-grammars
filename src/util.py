from typing import Dict
import itertools as it
from model import Node, Edge, NodeAttrs, EdgeAttrs
from graph import Graph

def basic_square(for_lhs=False, hanging=True):
    """
    for_lhs is mostly necessary when basic_* functions are invoked from
    __create_lhs - then handles are enumerated from 0, which is very
    handy during processing of monomorphisms.
    TODO: delete `hanging' argument after P7 is introduced and change it
    to false
    """
    graph = Graph()

    if for_lhs:
        node_1 = Node(NodeAttrs(label='v', x=0, y=0, hanging=False), handle=0)
        node_2 = Node(NodeAttrs(label='v', x=1, y=0, hanging=False), handle=1)
        node_3 = Node(NodeAttrs(label='v', x=1, y=1, hanging=False), handle=2)
        node_4 = Node(NodeAttrs(label='v', x=0, y=1, hanging=False), handle=3)
        node_q = Node(NodeAttrs(label='q', x=0.5, y=0.5, hanging=hanging), handle=4)
    else:
        node_1 = Node(NodeAttrs(label='v', x=0, y=0, hanging=False))
        node_2 = Node(NodeAttrs(label='v', x=1, y=0, hanging=False))
        node_3 = Node(NodeAttrs(label='v', x=1, y=1, hanging=False))
        node_4 = Node(NodeAttrs(label='v', x=0, y=1, hanging=False))
        node_q = Node(NodeAttrs(label='q', x=0.5, y=0.5, hanging=hanging))

    nodes = [node_1, node_2, node_3, node_4]

    graph.add_node_collection(nodes)
    graph.add_node(node_q)

    # add `edges' of hyperedge
    for node in nodes:
        attr = EdgeAttrs(kind='q', value=hanging)
        edge = Edge(node.handle, node_q.handle, attr)
        graph.add_edge(edge)

    # add boundry edges and set appropriate properties on them
    for node_a, node_b in it.pairwise(nodes + [node_1]):
        attr = EdgeAttrs(kind='e', value=True)
        edge = Edge(node_a.handle, node_b.handle, attr)
        graph.add_edge(edge)

    return graph

def basic_star5(for_lhs=False):
    """
    warning: star is facing to the left.
    """

    graph = Graph()

    if for_lhs:
        node_1 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_5 = Node(NodeAttrs('v', 1.3, 0.5, False), 4)
        node_p = Node(NodeAttrs('p', 0.5, 0.5, False), 5)
    else:
        node_1 = Node(NodeAttrs('v', 0, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 0, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        node_5 = Node(NodeAttrs('v', 1.3, 0.5, False))
        node_p = Node(NodeAttrs('p', 0.5, 0.5, False))

    nodes = [node_1, node_2, node_3, node_4, node_5]
    graph.add_node_collection(nodes)
    graph.add_node(node_p)

    for node in nodes:
        attr = EdgeAttrs('p', value=False)
        edge = Edge(node.handle, node_p.handle, attr)
        graph.add_edge(edge)

    return graph, nodes

def basic_pentagon(for_lhs=False):

    graph, nodes = basic_star5(for_lhs=for_lhs)
    idx_nodes = [0, 1, 4, 2, 3, 0]
    nodes_shuffled = [nodes[i] for i in idx_nodes]
    for node_a, node_b in it.pairwise(nodes_shuffled):
        attr = EdgeAttrs('e', value=True)
        edge = Edge(node_a.handle, node_b.handle, attr)
        graph.add_edge(edge)

    return graph


def reverse_dict_mapping(dictionary: Dict[int, int]) -> Dict[int, int]:
    return {v: k for k, v in dictionary.items()}


def verify_central_hyperedges(graph: 'Graph', nodes: list[Node]):
    edge_1_3 = graph.edge_for_handles(nodes[0].handle, nodes[2].handle)
    if edge_1_3.attrs.kind != 'q' or edge_1_3.attrs.value is False:
        return False

    edge_2_4 = graph.edge_for_handles(nodes[1].handle, nodes[3].handle)
    if edge_2_4.attrs.kind != 'q' or edge_2_4.attrs.value is False:
        return False

    if edge_1_3.attrs.handle != edge_2_4.attrs.handle:
        return False

    return True

