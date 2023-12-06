import unittest
import itertools as it
from copy import deepcopy

from graph import Graph
from model import Node, NodeAttrs, EdgeAttrs, Edge
from production import P1


class TestProduction1(unittest.TestCase):
    def test_production_can_be_applied_on_lhs_graph(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 0, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        nodes = [node_1, node_2, node_3, node_4]

        graph.add_node_collection(nodes)

        graph.add_edge(Edge(node_1.handle, node_3.handle, EdgeAttrs(kind='q', value=True)))
        graph.add_edge(Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='q', value=True)))

        for node_a, node_b in it.pairwise(nodes + [node_1]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', value=False)))

        p1 = P1()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p1.get_lhs())
        self.assertTrue(any(p1.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))

    def test_production_can_be_applied_on_more_complex_graph(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False))
        node_2 = Node(NodeAttrs('v', 0.5, 0, False))
        node_3 = Node(NodeAttrs('v', 1, 0, False))
        node_4 = Node(NodeAttrs('v', 1, 1, False))
        node_5 = Node(NodeAttrs('v', 0.5, 1, False))
        node_6 = Node(NodeAttrs('v', 0, 1, False))
        nodes = [node_1, node_2, node_3, node_4, node_5, node_6]

        graph.add_node_collection(nodes)

        graph.add_edge(Edge(node_1.handle, node_5.handle, EdgeAttrs(kind='q', value=True)))
        graph.add_edge(Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='q', value=True)))
        graph.add_edge(Edge(node_3.handle, node_5.handle, EdgeAttrs(kind='q', value=True)))
        graph.add_edge(Edge(node_2.handle, node_6.handle, EdgeAttrs(kind='q', value=True)))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', value=False)))
        for node_1, node_2 in it.pairwise(nodes + [node_1]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', value=False)))

        p1 = P1()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p1.get_lhs())
        self.assertTrue(any(p1.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))

    def test_production_cannot_be_applied_if_R_false(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 0, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        nodes = [node_1, node_2, node_3, node_4]

        graph.add_node_collection(nodes)

        graph.add_edge(Edge(node_1.handle, node_3.handle, EdgeAttrs(kind='q', value=False)))
        graph.add_edge(Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='q', value=True)))

        for node_a, node_b in it.pairwise(nodes + [node_1]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', value=False)))

        p1 = P1()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p1.get_lhs())
        self.assertFalse(any(p1.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))

    def test_production_cannot_be_applied_if_edge_types_not_match(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 0, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        nodes = [node_1, node_2, node_3, node_4]

        graph.add_node_collection(nodes)

        graph.add_edge(Edge(node_1.handle, node_3.handle, EdgeAttrs(kind='q', value=False)))
        graph.add_edge(Edge(node_2.handle, node_4.handle, EdgeAttrs(kind='q', value=True)))

        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='q', value=True)))
        for node_a, node_b in it.pairwise(nodes):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', value=False)))

        p1 = P1()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p1.get_lhs())
        self.assertFalse(any(p1.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))

if __name__ == '__main__':
    unittest.main()
