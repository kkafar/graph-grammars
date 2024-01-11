import itertools as it
import matplotlib.pyplot as plt
import util
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph
from .model import Production

class P17(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.hanging_node: Node | None = None
        self.external_nodes: list[Node] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs
    
    def requires_monomorphism(self) -> bool:
        return True

    def __create_lhs(self) -> Graph:
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 0, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        node_5 = Node(NodeAttrs('v', 1, 0.5, True))
        node_6 = Node(NodeAttrs('v', 2, 0.5, False))
        node_7 = Node(NodeAttrs('v', 2, 1, False))
        node_8 = Node(NodeAttrs('v', 0.5, 0, False))

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]
    
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False))
        graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', True))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

        # graph.display()
        # plt.show()

        return graph

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        # przerobić
        rev_mapping = self._rev_mapping

        # counter-clock-wise
        in_order_nodes = [graph.node_for_handle(rev_mapping[i]) for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)]
        corner_nodes = [in_order_nodes[0], in_order_nodes[1], in_order_nodes[2], in_order_nodes[3], in_order_nodes[7]]

        node_p = graph.node_for_handle(rev_mapping[8])

        # change hanging value of hanging node
        # we actualy have reference to this node, so we can modify it in place
        graph.remove_p_hyperedge(node_p.handle)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True), node_p.handle)