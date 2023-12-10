import itertools as it
import matplotlib.pyplot as plt
import util
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph
from .model import Production

class P11(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.hanging_node: Node | None = None
        self.external_nodes: list[Node] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def __create_lhs(self) -> Graph:
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 1.83, 0.5, False), 4)
        node_5 = Node(NodeAttrs('v', 0.5, 0, True), 5)
        node_6 = Node(NodeAttrs('v', 0, 0.5, True), 6)
        nodes = [node_0, node_5, node_1, node_4, node_2, node_3, node_6]
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True), 7)

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        # graph.display()
        # plt.show()

        return graph

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        rev_mapping = self._rev_mapping

        # counter-clock-wise
        in_order_nodes = [graph.node_for_handle(rev_mapping[i]) for i in (0, 1, 2, 3, 4, 5, 6, 7)]
        corner_nodes = [node for node in in_order_nodes[:-2]]
        
        hanging_node_1 = graph.node_for_handle(rev_mapping[5])
        hanging_node_2 = graph.node_for_handle(rev_mapping[6])
        q_node = graph.node_for_handle(rev_mapping[7])

        # change hanging value of hanging node
        # we actualy have reference to this node, so we can modify it in place
        hanging_node_1.attrs.flag = False
        hanging_node_2.attrs.flag = False
        new_border_nodes = []
        for node_a, node_b in ((in_order_nodes[1], in_order_nodes[4]), (in_order_nodes[4], in_order_nodes[2]), (in_order_nodes[2], in_order_nodes[3])):
            x, y = util.avg_point_from_nodes((node_a, node_b))
            edge_attrs = graph.edge_attrs((node_a.handle, node_b.handle))
            h = not edge_attrs.flag
            new_node = Node(NodeAttrs('v', x, y, h)) # has no handle, will be assigned when adding to graph
            new_border_nodes.append(new_node)

            graph.remove_edge(node_a.handle, node_b.handle)
            graph.add_node(new_node)
            graph.add_edge(Edge(u=node_a.handle, v=new_node.handle, attrs=EdgeAttrs('e', edge_attrs.flag)))
            graph.add_edge(Edge(u=new_node.handle, v=node_b.handle, attrs=EdgeAttrs('e', edge_attrs.flag)))

        # the central node
        # the central node
        x, y = util.avg_point_from_nodes(corner_nodes)
        central_node = Node(NodeAttrs('v', x, y, flag=False))
        graph.add_node(central_node)

        for node in new_border_nodes + [hanging_node_1, hanging_node_2]:
            graph.add_edge(Edge(node.handle, central_node.handle, EdgeAttrs('e', False)))
        
        graph.remove_p_hyperedge(q_node.handle)

        # # add Q edges
        # dokończyć
        assert len(new_border_nodes) == 3
        new_border_nodes.insert(0, hanging_node_1)
        new_border_nodes.append(hanging_node_2)

        for corner_node, new_nodes in zip(corner_nodes, it.pairwise([new_border_nodes[-1]] + new_border_nodes)):
            graph.add_q_hyperedge((corner_node, *new_nodes, central_node), EdgeAttrs('q', False))

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