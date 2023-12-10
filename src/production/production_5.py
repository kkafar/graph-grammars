import itertools as it
import matplotlib.pyplot as plt
import util
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph
from .model import Production


class P5(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None
        self.hanging_nodes: list[Node] | None = None
        self.external_nodes: list[Node] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def __create_lhs(self) -> Graph:
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 1, 0.5, True), 4)
        node_5 = Node(NodeAttrs('v', 0, 0.5, True), 5)
        node_6 = Node(NodeAttrs('v', 0.5, 0, True), 6)
        nodes = [node_0, node_6, node_1, node_4, node_2, node_3, node_5]
        corner_nodes = (node_0, node_1, node_2, node_3)

        graph.add_node_collection(nodes)

        graph.add_q_hyperedge(corner_nodes, EdgeAttrs('q', True), 7)

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        return graph

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        rev_mapping = self._rev_mapping

        in_order_nodes = [graph.node_for_handle(rev_mapping[i]) for i in range(8)]
        corner_nodes = [node for node in in_order_nodes[:4]]
        hanging_nodes = [graph.node_for_handle(rev_mapping[i]) for i in (6, 4, 5)]
        q_node = graph.node_for_handle(rev_mapping[7])

        # change hanging value of hanging nodes
        for hanging_node in hanging_nodes:
            hanging_node.attrs.flag = False

        # adding missing node
        node_a, node_b = in_order_nodes[2], in_order_nodes[3]
        x, y = util.avg_point_from_nodes((node_a, node_b))
        edge_attrs = graph.edge_attrs((node_a.handle, node_b.handle))
        h = not edge_attrs.flag
        new_border_node = Node(NodeAttrs('v', x, y, h)) # has no handle, will be assigned when adding to graph

        graph.remove_edge(node_a.handle, node_b.handle)
        graph.add_node(new_border_node)
        graph.add_edge(Edge(u=node_a.handle, v=new_border_node.handle, attrs=EdgeAttrs('e', edge_attrs.flag)))
        graph.add_edge(Edge(u=new_border_node.handle, v=node_b.handle, attrs=EdgeAttrs('e', edge_attrs.flag)))

        # the central node
        x, y = util.avg_point_from_nodes(corner_nodes)
        central_node = Node(NodeAttrs('v', x, y, flag=False))
        graph.add_node(central_node)

        for node in [new_border_node] + hanging_nodes:
            graph.add_edge(Edge(node.handle, central_node.handle, EdgeAttrs('e', False)))

        graph.remove_q_hyperedge(q_node.handle)

        # add Q edges
        hanging_nodes.insert(2, new_border_node)

        for corner_node, new_nodes in zip(corner_nodes, it.pairwise([hanging_nodes[-1]] + hanging_nodes)):
            graph.add_q_hyperedge((corner_node, *new_nodes, central_node), EdgeAttrs('q', False))

        # graph.display()
        # plt.show()
