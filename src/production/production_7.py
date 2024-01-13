import itertools as it
import matplotlib.pyplot as plt
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph
from .model import Production

class P7(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def requires_monomorphism(self):
        return True

    def reset(self):
        self.rev_mapping = None

    def __create_lhs(self) -> Graph:
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, None), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, None), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, None), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, None), 3)
        nodes = [node_0, node_1, node_2, node_3]
        graph.add_node_collection(nodes)
        graph.add_q_hyperedge(nodes, EdgeAttrs('q', False), 4)

        return graph

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        node_p = graph.node_for_handle(self._rev_mapping[4])
        graph.update_hyperedge_flag(node_p.handle, flag=True)

