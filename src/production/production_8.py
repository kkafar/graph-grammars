import itertools as it
import matplotlib.pyplot as plt
import util
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph
from .model import Production


class P8(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None
        self.hanging_nodes: list[Node] | None = None
        self.external_nodes: list[Node] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def requires_monomorphism(self):
        return True

    def __create_lhs(self) -> Graph:
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, None), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, None), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, None), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, None), 3)
        node_4 = Node(NodeAttrs('v', 1, 0.5, True), 4)
        node_5 = Node(NodeAttrs('v', 2, 0.5, None), 5)
        node_6 = Node(NodeAttrs('v', 2, 1, None), 6)
        nodes = [node_0, node_1, node_4, node_2, node_3, node_5, node_6]
        corner_nodes1 = (node_0, node_1, node_2, node_3)
        corner_nodes2 = (node_4, node_5, node_6, node_2)

        graph.add_node_collection(nodes)

        graph.add_q_hyperedge(corner_nodes1, EdgeAttrs('q', False), 7)
        graph.add_q_hyperedge(corner_nodes2, EdgeAttrs('q', True), 8)

        graph.add_edge(Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        return graph

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        rev_mapping = self._rev_mapping
        vertices = [
            graph.node_for_handle(rev_mapping[i]) for i in range(0, 7)
        ]
        node_p = graph.node_for_handle(rev_mapping[7])
        graph.update_hyperedge_flag(node_p.handle, flag=True)

