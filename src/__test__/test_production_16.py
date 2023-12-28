import unittest
import itertools as it

from matplotlib import pyplot as plt

from graph import Graph
from model import Node, NodeAttrs, EdgeAttrs, Edge
from basic_graph import basic_star5
from production.production_16 import P16

class TestProduction10(unittest.TestCase):
    def validate_shape_after_production(self, graph: Graph):
        self.assertTrue(graph.get_hyperedge_nodes()[0].attrs.flag)


    def test_production_can_be_applied_on_lhs_graph(self):
        graph, _ = basic_star5(for_lhs=True)
        
        res = P16()(graph)
        self.assertTrue(res)
        self.validate_shape_after_production(graph)
        
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
        
        graph.add_p_hyperedge((node_0, node_1, node_2, node_3, node_4), EdgeAttrs('p', False), p_node_coords=(0.5, 0.5))


        border_edges = [(node_0, node_1), (node_1, node_5), (node_5, node_6), (node_6, node_7), 
                 (node_7, node_2), (node_2, node_4), (node_4, node_3), (node_3, node_0)]
        
        shared_edges = [(node_1, node_2)]
    
        for _node_1, _node_2 in border_edges:
            graph.add_edge(Edge(_node_1.handle, _node_2.handle, EdgeAttrs(kind='e', flag=True)))

        for _node_1, _node_2 in shared_edges:
            graph.add_edge(Edge(_node_1.handle, _node_2.handle, EdgeAttrs(kind='e', flag=False)))

        
        res = P16()(graph)
        
        self.assertTrue(res)
        self.validate_shape_after_production(graph)
        

    def test_production_cannot_be_applied_if_R_true(self):
        graph, _ = basic_star5(for_lhs=True, select_central=True)
        
        res = P16()(graph)
        
        self.assertFalse(res)


if __name__ == '__main__':
    unittest.main()
