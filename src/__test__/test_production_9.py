import unittest

from matplotlib import pyplot as plt

from graph import Graph
from model import EdgeEndpoints, Node, NodeAttrs, EdgeAttrs, Edge
from production import P9

class TestProduction9(unittest.TestCase):
    def validate_shape_after_production(self, graph: Graph, previous_edges: list[Edge]):
        new_nodes = []
        for edge in previous_edges:
            node_1, node_2, flag = edge.u, edge.v, edge.attrs.flag
            v = graph.get_node_between((node_1, node_2))
            self.assertEqual(v.attrs.flag, not flag)
            new_nodes.append(v)
        
        center_node = graph.get_real_nodes()[-1]
        self.assertFalse(center_node.attrs.flag) # center node not hanging
        # center node connected to new nodes
        for node in new_nodes:
            self.assertTrue(graph.has_edge(EdgeEndpoints(node.handle, center_node.handle)))

    
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
        
        edges = graph.get_real_edges()
        
        res = P9()(graph)
        
        self.assertTrue(res)
        self.validate_shape_after_production(graph, edges)
        
        
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


        border_edges = [(node_0, node_1), (node_1, node_5), (node_5, node_6), (node_6, node_7), 
                 (node_7, node_2), (node_2, node_4), (node_4, node_3), (node_3, node_0)]
        
        shared_edges = [(node_1, node_2)]
    
        for node_1, node_2 in border_edges:
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=True)))

        for node_1, node_2 in shared_edges:
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))

        edges = graph.get_real_edges()
        
        res = P9()(graph)
        
        self.assertTrue(res)
        self.validate_shape_after_production(graph, filter(lambda edge: edge.u<5 and edge.v<5, edges)) # only left pentagon

    def test_production_cannot_be_applied_if_hanging(self):
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, True))
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
        
        self.assertFalse(P9()(graph))
        
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
        
        self.assertFalse(P9()(graph))



if __name__ == '__main__':
    unittest.main()
