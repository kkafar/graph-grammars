import itertools as it
import matplotlib.pyplot as plt
import util
import basic_graph
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph
from .model import Production

class P16(Production):
    def __init__(self, idx=None) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None
        self.idx: NodeHandle = idx

    def get_lhs(self) -> Graph:
        return self.lhs

    def requires_monomorphism(self):
        return True

    def reset(self):
        self.rev_mapping = None

    def __create_lhs(self) -> Graph:
#       graph, _ = util.basic_star5(for_lhs=True, select_central=False)
        graph, _ = basic_graph.basic_star5(for_lhs=True, select_central=False)
        return graph

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        # Break the edges (1, 2), (2, 3), (3, 4), (4, 1), creating 4 new nodes
        # Add 5 new node to the center of the split
        self.rev_mapping = util.reverse_dict_mapping(mapping)

        # Aliasing for convenience
        rev_mapping = self.rev_mapping

        # get square's vertices
        vertices = [
            graph.node_for_handle(rev_mapping[i]) for i in range(0, 5)
        ]

        # get inner node, the hyperedge
        node_p = graph.node_for_handle(rev_mapping[5])
    
        node_p.attrs.flag = True

        # graph.display()
        # plt.show()
