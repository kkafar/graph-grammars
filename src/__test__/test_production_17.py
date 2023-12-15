import unittest
import itertools as it

from graph import Graph
from model import Node, NodeAttrs, EdgeAttrs, Edge
from production import P17


class TestProduction17(unittest.TestCase):
    def is_any_mapping_feasible(self, graph: Graph):
        p17 = P17()
        mapping_gen = graph.generate_subgraphs_isomorphic_with(p17.get_lhs())
        return any(p17.is_mapping_feasible(graph, mapping) for mapping in mapping_gen)

    def test_production_can_be_applied_on_lhs_graph(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        node_5 = Node(NodeAttrs('v', 1, 0.5, True), 5)
        node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
        node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
        node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]
    
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False), 9)
        graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', True))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

        # left side edges
        graph.add_edge(Edge(node_1.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_8.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_3.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        # right side edges
        graph.add_edge(Edge(node_3.handle, node_7.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_7.handle, node_6.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_6.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
            
        self.assertTrue(self.is_any_mapping_feasible(graph))

    def test_production_can_be_applied_on_more_complex_graph(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        node_5 = Node(NodeAttrs('v', 1, 0.5, True), 5)
        node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
        node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
        node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

        # extra nodes
        node_10 = Node(NodeAttrs('v', -1, 0, False), 10)
        node_11 = Node(NodeAttrs('v', -1, 1, False), 11)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_10, node_11]
    
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False), 9)
        graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', True))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))
        
        # left side edges
        graph.add_edge(Edge(node_1.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_8.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_3.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        # right side edges
        graph.add_edge(Edge(node_3.handle, node_7.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_7.handle, node_6.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_6.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))

        # extra edges
        graph.add_edge(Edge(node_1.handle, node_10.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_10.handle, node_11.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_11.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertTrue(self.is_any_mapping_feasible(graph))
    
    def test_production_cannot_be_applied_if_R_false(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        node_5 = Node(NodeAttrs('v', 1, 0.5, True), 5)
        node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
        node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
        node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]
    
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False), 9)
        graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', False))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

        # left side edges
        graph.add_edge(Edge(node_1.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_8.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_3.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        # right side edges
        graph.add_edge(Edge(node_3.handle, node_7.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_7.handle, node_6.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_6.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        
        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_edge_types_not_match(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        node_5 = Node(NodeAttrs('v', 1, 0.5, True), 5)
        node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
        node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
        node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]
    
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False), 9)
        graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', True))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='p', flag=False)))
        graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

        # left side edges
        graph.add_edge(Edge(node_1.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_8.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_3.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        # right side edges
        graph.add_edge(Edge(node_3.handle, node_7.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_7.handle, node_6.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_6.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_one_hanging_node_is_missing(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        node_5 = Node(NodeAttrs('v', 1, 0.5, False), 5)
        node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
        node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
        node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]
    
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False), 9)
        graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', True))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

        # left side edges
        graph.add_edge(Edge(node_1.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_8.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_3.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        # right side edges
        graph.add_edge(Edge(node_3.handle, node_7.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_7.handle, node_6.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_6.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_p_hyperedge_is_missing(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        node_5 = Node(NodeAttrs('v', 1, 0.5, True), 5)
        node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
        node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
        node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]
    
        graph.add_node_collection(nodes)

        graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', True))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

        # left side edges
        graph.add_edge(Edge(node_1.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_8.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_3.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        # right side edges
        graph.add_edge(Edge(node_3.handle, node_7.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_7.handle, node_6.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_6.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_q_hyperedge_is_missing(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        node_5 = Node(NodeAttrs('v', 1, 0.5, True), 5)
        node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
        node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
        node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]
    
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False), 9)

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

        # left side edges
        graph.add_edge(Edge(node_1.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_8.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_3.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        # right side edges
        graph.add_edge(Edge(node_3.handle, node_7.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_7.handle, node_6.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_6.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))

        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_one_hanging_node_is_in_wrong_place(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, True), 1)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        node_5 = Node(NodeAttrs('v', 1, 0.5, False), 5)
        node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
        node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
        node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]
    
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False), 9)
        graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', True))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

        # left side edges
        graph.add_edge(Edge(node_1.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_8.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_3.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        # right side edges
        graph.add_edge(Edge(node_3.handle, node_7.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_7.handle, node_6.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_6.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
            
        self.assertFalse(self.is_any_mapping_feasible(graph))

    def test_production_cannot_be_applied_if_one_more_node_is_hanging(self):
        graph = Graph()

        node_1 = Node(NodeAttrs('v', 0, 0, True), 1)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 2)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 4)
        node_5 = Node(NodeAttrs('v', 1, 0.5, True), 5)
        node_6 = Node(NodeAttrs('v', 2, 0.5, False), 6)
        node_7 = Node(NodeAttrs('v', 2, 1, False), 7)
        node_8 = Node(NodeAttrs('v', 0.5, 0, False), 8)

        nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8]
    
        graph.add_node_collection(nodes)

        graph.add_p_hyperedge([node_1, node_2, node_3, node_4, node_8], EdgeAttrs('p', False), 9)
        graph.add_q_hyperedge([node_5, node_6, node_7, node_3], EdgeAttrs('q', True))

        graph.add_edge(Edge(node_2.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_5.handle, node_3.handle, EdgeAttrs(kind='e', flag=False)))

        # left side edges
        graph.add_edge(Edge(node_1.handle, node_8.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_8.handle, node_2.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_3.handle, node_4.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_4.handle, node_1.handle, EdgeAttrs(kind='e', flag=False)))

        # right side edges
        graph.add_edge(Edge(node_3.handle, node_7.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_7.handle, node_6.handle, EdgeAttrs(kind='e', flag=False)))
        graph.add_edge(Edge(node_6.handle, node_5.handle, EdgeAttrs(kind='e', flag=False)))
            
        self.assertFalse(self.is_any_mapping_feasible(graph))


if __name__ == '__main__':
    unittest.main()