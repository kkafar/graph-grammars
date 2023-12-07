from typing import Dict
import itertools as it
from model import Node
from graph import Graph


def reverse_dict_mapping(dictionary: Dict[int, int]) -> Dict[int, int]:
    return {v: k for k, v in dictionary.items()}


def verify_central_hyperedges(graph: 'Graph', nodes: list[Node]):
    edge_1_3 = graph.edge_for_handles(nodes[0].handle, nodes[2].handle)
    if edge_1_3.attrs.kind != 'q' or edge_1_3.attrs.value is False:
        return False

    edge_2_4 = graph.edge_for_handles(nodes[1].handle, nodes[3].handle)
    if edge_2_4.attrs.kind != 'q' or edge_2_4.attrs.value is False:
        return False
    return True

