import unittest
import itertools as it

from matplotlib import pyplot as plt

from graph import Graph
from model import Node, NodeAttrs, EdgeAttrs, Edge
from basic_graph import basic_star5
from production.production_7 import P7

class TestProduction10(unittest.TestCase):
    def validate_q_R_true(self, graph: Graph):
        self.assertTrue(graph.get_hyperedge_nodes()[0].attrs.flag)

    def test_production_can_be_applied_on_lhs_graph(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        nodes = [node_0, node_1, node_2, node_3]
        graph.add_node_collection(nodes)
        graph.add_q_hyperedge(nodes, EdgeAttrs('q', False), 4)
        
        res = P7()(graph)
        self.assertTrue(res)
        self.validate_q_R_true(graph)
        
    def test_production_cannot_be_applied_if_R_true(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        nodes = [node_0, node_1, node_2, node_3]
        graph.add_node_collection(nodes)
        graph.add_q_hyperedge(nodes, EdgeAttrs('q', True), 4)
        
        res = P7()(graph)
        
        self.assertFalse(res)

    def test_production_can_be_applied_on_p1_graph_with_R_false(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 0, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        nodes = [node_1, node_2, node_3, node_4]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_1, node_2, node_3, node_4), EdgeAttrs('q', False))

        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='q', flag=True)))
        for node_a, node_b in it.pairwise(nodes):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        res = P7()(graph)
        
        self.assertTrue(res)
        self.validate_q_R_true(graph)

    def test_production_can_be_applied_on_p2_graph_with_R_false(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1, 0.5, True))
        nodes = [node_0, node_1, node_4, node_2, node_3]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', False))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        res = P7()(graph)
        
        self.assertTrue(res)
        self.validate_q_R_true(graph)

    def test_production_can_be_applied_on_p3_graph_with_R_false(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1, 0.5, True))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        nodes = [node_0, node_5, node_1, node_4, node_2, node_3]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', False))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        res = P7()(graph)
        
        self.assertTrue(res)
        self.validate_q_R_true(graph)

    def test_production_can_be_applied_on_p4_graph_with_R_false(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 0.5, 1, True))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        nodes = [node_0, node_5, node_1, node_2, node_4, node_3]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', False))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        res = P7()(graph)
        
        self.assertTrue(res)
        self.validate_q_R_true(graph)

    def test_production_can_be_applied_on_p5_graph_with_R_false(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1, 0.5, True))
        node_5 = Node(NodeAttrs('v', 0, 0.5, True))
        node_6 = Node(NodeAttrs('v', 0.5, 0, True))
        nodes = [node_0, node_6, node_1, node_4, node_2, node_3, node_5]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', False))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        res = P7()(graph)
        
        self.assertTrue(res)
        self.validate_q_R_true(graph)

    def test_production_can_be_applied_on_p6_graph_with_R_false(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1, 0.5, True))
        node_5 = Node(NodeAttrs('v', 0.5, 1, True))
        node_6 = Node(NodeAttrs('v', 0, 0.5, True))
        node_7 = Node(NodeAttrs('v', 0.5, 0, True))
        nodes = [node_0, node_7, node_1, node_4, node_2, node_5, node_3, node_6]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', False))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        res = P7()(graph)
        
        self.assertTrue(res)
        self.validate_q_R_true(graph)

if __name__ == '__main__':
    unittest.main()
