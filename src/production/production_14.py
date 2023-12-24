import itertools as it
import matplotlib.pyplot as plt
import util
from typing import Dict
import basic_graph
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph
from .model import Production


class P14(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def __create_lhs(self) -> Graph:
        graph = Graph()

        # Not hanging nodes
        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1.5, 0.5, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        # Hanging nodes
        node_5 = Node(NodeAttrs('v', 0.5, 0, True), 5)
        node_6 = Node(NodeAttrs('v', 0.5, 1, True), 6)
        node_7 = Node(NodeAttrs('v', 0, 0.5, True), 7)
        node_8 = Node(NodeAttrs('v', 1.25, 0.75, True), 8)
        nodes = [node_0, node_5, node_1, node_2, node_8, node_3, node_6, node_4, node_7]
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True), 9)

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        return graph

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        rev_mapping = self._rev_mapping

        corner_nodes = [graph.node_for_handle(rev_mapping[i]) for i in range(5)]
        hanging_nodes = [graph.node_for_handle(rev_mapping[i]) for i in [5, 6, 7, 8]]

        # change hanging value of hanging nodes
        for h_node in hanging_nodes:
            h_node.attrs.flag = False

        # split two edges with new hanging nodes
        edge_1_2_flag = graph.edge_for_handles(corner_nodes[1].handle, corner_nodes[2].handle).attrs.flag
        node_9 = graph.split_edge_with_vnode(((corner_nodes[1].handle, corner_nodes[2].handle)), not edge_1_2_flag)

        # remove p-hyperedge...
        p_node = graph.node_for_handle(rev_mapping[9])
        graph.remove_p_hyperedge(p_node.handle)

        # ...and replace it with central node
        central_node = Node(NodeAttrs('v', p_node.attrs.x, p_node.attrs.y, False))
        graph.add_node(central_node)

        # reorganise hanging nodes list for easier quadrilaterals creation
        hanging_nodes = [hanging_nodes[0], node_9, hanging_nodes[3], hanging_nodes[1], hanging_nodes[2]]

        # create 5 e-edges
        for h_node in hanging_nodes:
            graph.add_edge(Edge(h_node.handle, central_node.handle, EdgeAttrs('e', True)))

        # create 5 q-edges
        for i in range(5):
            q_edge_nodes = [corner_nodes[i], hanging_nodes[i], central_node, hanging_nodes[(i - 1) % 5]]
            graph.add_q_hyperedge(q_edge_nodes, EdgeAttrs('q', False))
