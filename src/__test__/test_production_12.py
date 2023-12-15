import unittest
import itertools as it

from graph import Graph
from model import Node, NodeAttrs, EdgeAttrs, Edge
from production import P12


class TestProduction12(unittest.TestCase):
    def is_any_mapping_feasible(self, graph: Graph):
        p12 = P12()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p12.get_lhs())
        return any(p12.is_mapping_feasible(graph, mapping) for mapping in mapping_gen)

    def test_production_can_be_applied_on_lhs_graph(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 1.83, 0.5, False), 4)
        node_5 = Node(NodeAttrs('v', 0.5, 0, True), 5)
        node_6 = Node(NodeAttrs('v', 0.5, 1, True), 6)
        nodes = [node_0, node_5, node_1, node_4, node_2, node_6, node_3]
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True), 7)

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))
            
        self.assertTrue(self.is_any_mapping_feasible(graph))

    def test_production_can_be_applied_on_more_complex_graph(self):
        graph = Graph()

        node_8 = Node(NodeAttrs('v', -1, 0, True), 8)
        node_9 = Node(NodeAttrs('v', -1, 1, True), 9)

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1.83, 0.5, False))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        nodes = [node_0, node_5, node_1, node_4, node_2, node_6, node_3, node_8, node_9]
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True), 7)

        for node_a, node_b in it.pairwise(nodes[:-2] + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))
        
        graph.add_edge(Edge(node_0.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_8.handle, node_9.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_9.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))
        self.assertTrue(self.is_any_mapping_feasible(graph))
    
    def test_production_cannot_be_applied_if_R_false(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1.83, 0.5, False))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        nodes = [node_0, node_5, node_1, node_4, node_2, node_6, node_3]
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', False))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))
        
        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_edge_types_not_match(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1.83, 0.5, False))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        nodes = [node_0, node_5, node_1, node_4, node_2, node_6, node_3]
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='p', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_one_hanging_node_is_missing(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1.83, 0.5, False))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, False))
        nodes = [node_0, node_5, node_1, node_4, node_2, node_6, node_3]
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_p_hyperedge_is_missing(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1.83, 0.5, False))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        nodes = [node_0, node_5, node_1, node_4, node_2, node_6, node_3]
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        graph.add_node_collection(nodes)

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_one_hanging_node_is_in_wrong_place(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, True))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1.83, 0.5, False))
        node_5 = Node(NodeAttrs('v', 0.5, 0, False))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        nodes = [node_0, node_5, node_1, node_4, node_2, node_6, node_3]
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_one_more_node_is_hanging(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 1.83, 0.5, True))
        node_5 = Node(NodeAttrs('v', 0.5, 0, True))
        node_6 = Node(NodeAttrs('v', 0.5, 1, True))
        nodes = [node_0, node_5, node_1, node_4, node_2, node_6, node_3]
        corner_nodes = (node_0, node_1, node_2, node_3, node_4)

        graph.add_node_collection(nodes)

        graph.add_p_hyperedge(corner_nodes, EdgeAttrs('p', True))

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))


if __name__ == '__main__':
    unittest.main()