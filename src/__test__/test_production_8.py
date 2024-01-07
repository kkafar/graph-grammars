import unittest
import itertools as it
from matplotlib import pyplot as plt
from graph import Graph
from model import Node, NodeAttrs, EdgeAttrs, Edge
from production import P8


class TestProduction8(unittest.TestCase):
    def validate_shape_after_production(self, graph: Graph):
        self.assertTrue(graph.get_hyperedge_nodes()[0].attrs.flag)

    def test_production_can_be_applied_on_lhs_graph(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 1, 0.5, True), 4)
        node_5 = Node(NodeAttrs('v', 2, 0.5, False), 5)
        node_6 = Node(NodeAttrs('v', 2, 1, False), 6)
        nodes = [node_0, node_1, node_4, node_2, node_3, node_5, node_6]
        corner_nodes1 = (node_0, node_1, node_2, node_3)
        corner_nodes2 = (node_4, node_5, node_6, node_2)

        graph.add_node_collection(nodes)

        graph.add_q_hyperedge(corner_nodes1, EdgeAttrs('q', False), 7)
        graph.add_q_hyperedge(corner_nodes2, EdgeAttrs('q', True), 8)

        graph.add_edge(Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        res = P8()(graph)
        self.assertTrue(res)
        self.validate_shape_after_production(graph)

    def test_production_cannot_be_applied_if_both_R_false(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 1, 0.5, True), 4)
        node_5 = Node(NodeAttrs('v', 2, 0.5, False), 5)
        node_6 = Node(NodeAttrs('v', 2, 1, False), 6)
        nodes = [node_0, node_1, node_4, node_2, node_3, node_5, node_6]
        corner_nodes1 = (node_0, node_1, node_2, node_3)
        corner_nodes2 = (node_4, node_5, node_6, node_2)

        graph.add_node_collection(nodes)

        graph.add_q_hyperedge(corner_nodes1, EdgeAttrs('q', False), 7)
        graph.add_q_hyperedge(corner_nodes2, EdgeAttrs('q', False), 8)

        graph.add_edge(Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        res = P8()(graph)

        self.assertFalse(res)

    def test_production_cannot_be_applied_if_R_true(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 1, 0.5, True), 4)
        node_5 = Node(NodeAttrs('v', 2, 0.5, False), 5)
        node_6 = Node(NodeAttrs('v', 2, 1, False), 6)
        nodes = [node_0, node_1, node_4, node_2, node_3, node_5, node_6]
        corner_nodes1 = (node_0, node_1, node_2, node_3)
        corner_nodes2 = (node_4, node_5, node_6, node_2)

        graph.add_node_collection(nodes)

        graph.add_q_hyperedge(corner_nodes1, EdgeAttrs('q', True), 7)
        graph.add_q_hyperedge(corner_nodes2, EdgeAttrs('q', True), 8)

        graph.add_edge(Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        res = P8()(graph)

        self.assertFalse(res)

    def test_production_cannot_be_applied_if_no_hanging_nodes(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 1, 0.5, False), 4)
        node_5 = Node(NodeAttrs('v', 2, 0.5, False), 5)
        node_6 = Node(NodeAttrs('v', 2, 1, False), 6)
        nodes = [node_0, node_1, node_4, node_2, node_3, node_5, node_6]
        corner_nodes1 = (node_0, node_1, node_2, node_3)
        corner_nodes2 = (node_4, node_5, node_6, node_2)

        graph.add_node_collection(nodes)

        graph.add_q_hyperedge(corner_nodes1, EdgeAttrs('q', True), 7)
        graph.add_q_hyperedge(corner_nodes2, EdgeAttrs('q', True), 8)

        graph.add_edge(Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        res = P8()(graph)

        self.assertFalse(res)


if __name__ == '__main__':
    unittest.main()
