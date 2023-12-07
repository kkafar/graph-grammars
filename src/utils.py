import itertools as it
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph


def verify_central_hyperedges(graph: 'Graph', nodes: list[Node]):
    edge_1_3 = graph.edge_for_handles(nodes[0].handle, nodes[2].handle)
    if edge_1_3.attrs.kind != 'q' or edge_1_3.attrs.value is False:
        return False

    edge_2_4 = graph.edge_for_handles(nodes[1].handle, nodes[3].handle)
    if edge_2_4.attrs.kind != 'q' or edge_2_4.attrs.value is False:
        return False
    return True


def verify_normal_edges_type(graph: 'Graph', nodes: list[Node]):
    for node_a, node_b in it.pairwise(nodes + [nodes[0]]):
        print(node_a, node_b)
        edge = graph.edge_for_handles(node_a.handle, node_b.handle)
        if edge.attrs.kind != 'e':
            return False
    return True
