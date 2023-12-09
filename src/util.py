from typing import Dict, Iterable
import itertools as it
from model import Node


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

# TODO: Type this properly
def iter_batched(iterable: Iterable, n: int):
    assert n >= 1
    iterator = iter(iterable)
    while batch := tuple(it.islice(iterator, n)):
        yield batch


def avg_point_from_nodes(nodes: Iterable[Node]) -> tuple[float, float]:
    count = len(nodes)
    x = sum(map(lambda node: node.attrs.x, nodes)) / count
    y = sum(map(lambda node: node.attrs.y, nodes)) / count
    return (x, y)

