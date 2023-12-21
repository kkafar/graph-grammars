import unittest
import itertools as it

from graph import Graph
from model import Node, NodeAttrs, EdgeAttrs, Edge

from production import P3

class TestProduction2(unittest.TestCase):
    def test_production_can_be_applied_on_lhs_graph(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1, 0.5, True))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        nodes = [node_0, node_5, node_1, node_4, node_2, node_3]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', True))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        p3 = P3()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p3.get_lhs())
        self.assertTrue(any(p3.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))

    def test_production_can_be_applied_if_hanging_nodes_in_different_places(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1, 0.5, True))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        nodes = [node_0, node_1, node_4, node_2, node_5, node_3]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', True))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        p3 = P3()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p3.get_lhs())
        self.assertTrue(any(p3.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))

    def test_production_cannot_be_applied_with_one_hanging_node(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1, 0.5, True))
        nodes = [node_0, node_1, node_4, node_2, node_3]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', True))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        p3 = P3()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p3.get_lhs())
        self.assertFalse(any(p3.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))

    def test_production_cannot_be_applied_with_two_hanging_nodes_on_opposite_sides(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1, 0.5, True))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        nodes = [node_0, node_1, node_4, node_2, node_3, node_5]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', True))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        p3 = P3()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p3.get_lhs())
        self.assertFalse(any(p3.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))

    def test_production_can_be_applied_on_more_complex_graph(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False))
        node_2 = Node(NodeAttrs('v', 0.5, 0, False))
        node_3 = Node(NodeAttrs('v', 1, 0, False))
        node_4 = Node(NodeAttrs('v', 1, 1, False))
        node_5 = Node(NodeAttrs('v', 0.5, 1, False))
        node_6 = Node(NodeAttrs('v', 0, 1, False))
        node_7 = Node(NodeAttrs('v', 0.25, 0, True))
        node_8 = Node(NodeAttrs('v', 0, 0.25, True))
        nodes = [node_1, node_7, node_2, node_3, node_4, node_5, node_6, node_8]

        graph.add_node_collection(nodes)

        graph.add_q_hyperedge((node_1, node_5, node_2, node_6), EdgeAttrs('q', True))
        graph.add_q_hyperedge((node_2, node_4, node_3, node_5), EdgeAttrs('q', True))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        for node_1, node_2 in it.pairwise(nodes + [node_1]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        p3 = P3()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p3.get_lhs())
        self.assertTrue(any(p3.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))

    def test_production_cannot_be_applied_if_R_false(self):
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

        p3 = P3()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p3.get_lhs())
        self.assertFalse(any(p3.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))

    def test_production_cannot_be_applied_if_edge_types_not_match(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1, 0.5, True))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        nodes = [node_0, node_5, node_1, node_4, node_2, node_3]

        graph.add_node_collection(nodes)
        graph.add_q_hyperedge((node_0, node_1, node_2, node_3), EdgeAttrs('q', True))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='q', flag=False)))

        p3 = P3()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p3.get_lhs())
        self.assertFalse(any(p3.is_mapping_feasible(graph, mapping) for mapping in mapping_gen))


if __name__ == '__main__':
    unittest.main()
