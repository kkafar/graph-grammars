import itertools as it
import matplotlib.pyplot as plt
import util
import basic_graph
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph
from .model import Production

class P9(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def reset(self):
        self.rev_mapping = None

    def requires_monomorphism(self):
        return True

    def __create_lhs(self) -> Graph:
#       return util.basic_pentagon(for_lhs=True, select_central=True)
        return basic_graph.basic_pentagon(for_lhs=True, select_central=True)

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
        idx_nodes = [0, 1, 4, 2, 3, 0]
        nodes_shuffled = [vertices[idx] for idx in idx_nodes]

        new_boundary = []
        for node_a, node_b in it.pairwise(nodes_shuffled):
            edge = (node_a.handle, node_b.handle)
            edge_attrs = graph.edge_attrs(edge)
            hanging = not edge_attrs.flag
            new_node = graph.split_edge_with_vnode(edge, node_flag=hanging)
            new_boundary.append(new_node)

        graph.remove_p_hyperedge(node_p.handle)

        x = node_p.attrs.x
        y = node_p.attrs.y
        central = Node(NodeAttrs('v', x, y, flag=False), node_p.handle)
        graph.add_node(central)

        for new_node in new_boundary:
            attr = EdgeAttrs('e', False)
            edge = Edge(new_node.handle, central.handle, attr)
            graph.add_edge(edge)

        # create inner nodes and connect new nodes on the boundry with inner nodes
        inner_nodes = []
        for vert, (node_a, node_b) in zip(nodes_shuffled, it.pairwise([new_boundary[-1]] + new_boundary)):
            nodes = (vert, node_a, node_b, central)
            attr = EdgeAttrs('q', False)
            graph.add_q_hyperedge(nodes, edge_attrs=attr)

