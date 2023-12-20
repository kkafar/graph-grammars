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

    def __create_lhs(self) -> Graph:
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        node_5 = Node(NodeAttrs('v', 1, 0.5, True), 5)
        node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
        node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
        node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]
    
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False), 9)
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
        corner_nodes = [in_order_nodes[1], in_order_nodes[2], in_order_nodes[3], in_order_nodes[4], in_order_nodes[8]]

        node_p = graph.node_for_handle(rev_mapping[9])

        # change hanging value of hanging node
        # we actualy have reference to this node, so we can modify it in place
        graph.remove_p_hyperedge(node_p.handle)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True), 9)

        # edges printing to check if graph was changed properly
        nodes = graph.nx_graph.nodes.data()
        count_node_q, count_node_v = 0, 0
        for node in nodes:
            if node[1]['payload'].label == 'q': count_node_q += 1
            if node[1]['payload'].label == 'v': count_node_v += 1

        edges = graph.nx_graph.edges.data()
        count_e, count_p, count_q = 0, 0, 0
        for edge in edges:
            if edge[2]['payload'].kind == 'e': count_e += 1
            if edge[2]['payload'].kind == 'p': count_p += 1
            if edge[2]['payload'].kind == 'q': count_q += 1

        print(f"Number of nodes: {len(nodes)}")
        print(f"count_node_q: {count_node_q}, count_node_v: {count_node_v}")
        print(f"Number of edges: {len(edges)}")
        print(f"count_e: {count_e}, count_p: {count_p}, count_q: {count_q}")
        # graph.display()
        # plt.show()