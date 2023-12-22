import unittest
import itertools as it

from matplotlib import pyplot as plt

from graph import Graph
from model import Node, NodeAttrs, EdgeAttrs, Edge
from production import P10
from basic_graph import basic_pentagon

class TestProduction10(unittest.TestCase):
    def is_any_mapping_feasible(self, graph: Graph):
        p10 = P10()
        mapping_gen = graph.generate_subgraphs_monomorphic_with(p10.get_lhs())
        return any(p10.is_mapping_feasible(graph, mapping) for mapping in mapping_gen)

    def test_production_can_be_applied_on_lhs_graph(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        
        node_4 = Node(NodeAttrs('v', 1.5, 0.5, False))
        nodes = [node_0, node_1, node_2, node_3, node_4]

        graph.add_node_collection(nodes)
        graph.add_p_hyperedge((node_0, node_1, node_2, node_3, node_4), EdgeAttrs('p', True), p_node_coords=(0.5, 0.5))
        
        edges = [(node_0, node_1), (node_1, node_4), (node_4, node_2), (node_2, node_3), (node_3, node_0)]
        for node_1, node_2 in edges:
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=True)))
        
        graph.split_edge_with_vnode(edge=(0, 1), node_flag=True)
        self.assertTrue(self.is_any_mapping_feasible(graph))
        
    def test_production_can_be_applied_on_more_complex_graph(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        node_4 = Node(NodeAttrs('v', 0.5, 1.5, False))
        
        node_5 = Node(NodeAttrs('v', 2, 0, False)) 
        node_6 = Node(NodeAttrs('v', 2, 1, False))
        node_7 = Node(NodeAttrs('v', 1.5, 1.5, False))

        nodes = [node_0, node_1, node_2, node_3, node_4, node_5, node_6, node_7] 
        graph.add_node_collection(nodes)
        
        graph.add_p_hyperedge((node_0, node_1, node_2, node_3, node_4), EdgeAttrs('p', True), p_node_coords=(0.5, 0.5))
        graph.add_p_hyperedge((node_5, node_6, node_2, node_3, node_7), EdgeAttrs('p', True), p_node_coords=(1.5, 0.5))


        edges = [(node_0, node_1), (node_1, node_4), (node_4, node_2), (node_3, node_0), 
                 (node_5, node_6), (node_6, node_7), (node_7, node_2), (node_2, node_5)]
        
        graph.add_edge(Edge(node_2.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

        for node_1, node_2 in edges:
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=True)))

        graph.split_edge_with_vnode(edge=(0, 1), node_flag=True)
        self.assertTrue(self.is_any_mapping_feasible(graph))
        
    def test_node_no_longer_hanging_after_production_applied(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        
        node_4 = Node(NodeAttrs('v', 1.5, 0.5, False))
        nodes = [node_0, node_1, node_2, node_3, node_4]

        graph.add_node_collection(nodes)
        graph.add_p_hyperedge((node_0, node_1, node_2, node_3, node_4), EdgeAttrs('p', True), p_node_coords=(0.5, 0.5))
        
        edges = [(node_0, node_1), (node_1, node_4), (node_4, node_2), (node_2, node_3), (node_3, node_0)]
        for node_1, node_2 in edges:
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=True)))
        
        graph.split_edge_with_vnode(edge=(0, 1), node_flag=True)
        
        
        P10()(graph)

        self.assertFalse(graph.node_attrs(6).flag)

    def test_production_cannot_be_applied_if_no_hanging(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        
        node_4 = Node(NodeAttrs('v', 1.5, 0.5, False))
        nodes = [node_0, node_1, node_2, node_3, node_4]

        graph.add_node_collection(nodes)
        graph.add_p_hyperedge((node_0, node_1, node_2, node_3, node_4), EdgeAttrs('p', True), p_node_coords=(0.5, 0.5))
        
        edges = [(node_0, node_1), (node_1, node_4), (node_4, node_2), (node_2, node_3), (node_3, node_0)]
        for node_1, node_2 in edges:
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=True)))
        
        graph.split_edge_with_vnode(edge=(0, 1), node_flag=False)
        self.assertFalse(self.is_any_mapping_feasible(graph))
        
    def test_production_cannot_be_applied_if_R_false(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False))
        node_1 = Node(NodeAttrs('v', 1, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 1, False))
        node_3 = Node(NodeAttrs('v', 0, 1, False))
        
        node_4 = Node(NodeAttrs('v', 1.5, 0.5, False))
        nodes = [node_0, node_1, node_2, node_3, node_4]

        graph.add_node_collection(nodes)
        graph.add_p_hyperedge((node_0, node_1, node_2, node_3, node_4), EdgeAttrs('p', False), p_node_coords=(0.5, 0.5))
        
        edges = [(node_0, node_1), (node_1, node_4), (node_4, node_2), (node_2, node_3), (node_3, node_0)]
        for node_1, node_2 in edges:
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=True)))
        
        graph.split_edge_with_vnode(edge=(0, 1), node_flag=True)
        self.assertFalse(self.is_any_mapping_feasible(graph))


if __name__ == '__main__':
    unittest.main()
