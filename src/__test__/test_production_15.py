import unittest
import itertools as it

from graph import Graph
from model import Node, NodeAttrs, EdgeAttrs, Edge
from production import P15


class TestProduction15(unittest.TestCase):

    def is_any_mapping_feasible(self, graph: Graph):
        p15 = P15()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p15.get_lhs())
        return any(p15.is_mapping_feasible(graph, mapping) for mapping in mapping_gen)

    def test_production_can_be_applied_on_lhs_graph(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1.5, 0.5, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        node_7 = Node(NodeAttrs('v', 0, 0.5, True))
        node_8 = Node(NodeAttrs('v', 1.25, 0.75, True))
        node_9 = Node(NodeAttrs('v', 1.25, 0.25, True))
        nodes = [node_0, node_5, node_1, node_9, node_2, node_8, node_3, node_6, node_4, node_7]
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertTrue(self.is_any_mapping_feasible(graph))

    def test_production_can_be_applied_on_more_complex_graph(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1.5, 0.5, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        node_7 = Node(NodeAttrs('v', 0, 0.5, True))
        node_8 = Node(NodeAttrs('v', 1.25, 0.75, True))
        node_9 = Node(NodeAttrs('v', 1.25, 0.25, True))
        nodes = [node_0, node_5, node_1, node_9, node_2, node_8, node_3, node_6, node_4, node_7]
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        node_extra = Node(NodeAttrs('v', 0.5, 1.5, False))
        graph.add_node(node_extra)
        graph.add_edge(Edge(node_extra.handle, node_3.handle, EdgeAttrs('e', False)))
        graph.add_edge(Edge(node_extra.handle, node_4.handle, EdgeAttrs('e', False)))

        self.assertTrue(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_R_false(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1.5, 0.5, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        node_7 = Node(NodeAttrs('v', 0, 0.5, True))
        node_8 = Node(NodeAttrs('v', 1.25, 0.75, True))
        node_9 = Node(NodeAttrs('v', 1.25, 0.25, True))
        nodes = [node_0, node_5, node_1, node_9, node_2, node_8, node_3, node_6, node_4, node_7]
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', False))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_edge_types_not_match(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1.5, 0.5, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        node_7 = Node(NodeAttrs('v', 0, 0.5, True))
        node_8 = Node(NodeAttrs('v', 1.25, 0.75, True))
        node_9 = Node(NodeAttrs('v', 1.25, 0.25, True))
        nodes = [node_0, node_5, node_1, node_9, node_2, node_8, node_3, node_6, node_4, node_7]
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='p', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_one_hanging_node_is_missing(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1.5, 0.5, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        node_7 = Node(NodeAttrs('v', 0, 0.5, True))
        node_8 = Node(NodeAttrs('v', 1.25, 0.75, True))
        nodes = [node_0, node_5, node_1, node_2, node_8, node_3, node_6, node_4, node_7]
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_p_hyperedge_is_missing(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1.5, 0.5, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        node_7 = Node(NodeAttrs('v', 0, 0.5, True))
        node_8 = Node(NodeAttrs('v', 1.25, 0.75, True))
        node_9 = Node(NodeAttrs('v', 1.25, 0.25, True))
        nodes = [node_0, node_5, node_1, node_9, node_2, node_8, node_3, node_6, node_4, node_7]
        graph.add_node_collection(nodes)

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_one_more_node_is_hanging(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1.5, 0.5, True))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        node_7 = Node(NodeAttrs('v', 0, 0.5, True))
        node_8 = Node(NodeAttrs('v', 1.25, 0.75, True))
        node_9 = Node(NodeAttrs('v', 1.25, 0.25, True))
        nodes = [node_0, node_5, node_1, node_9, node_2, node_8, node_3, node_6, node_4, node_7]
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))


if __name__ == '__main__':
    unittest.main()
