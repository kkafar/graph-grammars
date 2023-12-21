import unittest
import itertools as it

from graph import Graph
from model import Node, NodeAttrs, EdgeAttrs, Edge
from production import P9
from basic_graph import basic_pentagon

class TestProduction9(unittest.TestCase):
    def is_any_mapping_feasible(self, graph: Graph):
        p9 = P9()
        mapping_gen = graph.generate_subgraphs_monomorphic_with(p9.get_lhs())
        return any(p9.is_mapping_feasible(graph, mapping) for mapping in mapping_gen)

    def test_production_can_be_applied_on_lhs_graph(self):
        graph = basic_pentagon()


        self.assertTrue(self.is_any_mapping_feasible(graph))

   

if __name__ == '__main__':
    unittest.main()
