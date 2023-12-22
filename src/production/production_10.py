import itertools as it
import matplotlib.pyplot as plt
import util
import basic_graph
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph
from .model import Production

class P10(Production):
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
#       graph = util.basic_pentagon(for_lhs=True, select_central=True)
        graph = basic_graph.basic_pentagon(for_lhs=True, select_central=True)
        # handle is 6 because the interior is 5
        graph.split_edge_with_vnode(edge=(0, 1), node_flag=True, node_handle=6)
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
        node_h = graph.node_for_handle(rev_mapping[6])

        # you must get edges attrs before you remove, now it is relevant
        edge = vertices[0].handle, node_h.handle
        attrs = graph.edge_attrs(edge)
        is_boundary = attrs.flag
        hdl = node_h.handle
        graph.remove_node(node_h.handle)
        edge = vertices[0].handle, vertices[1].handle
        tmp_attr = EdgeAttrs('e', is_boundary, -1)
        # flag value is only valuable, because it will propagate through split
        tmp_edge = Edge(edge[0], edge[1], tmp_attr)
        graph.add_edge(tmp_edge)
        # change hanging atribute of the node
        hang = graph.split_edge_with_vnode(edge, node_flag=False, node_handle=hdl)
        
        # skip first pair because it already exists
        idx_nodes = [1, 4, 2, 3, 0]
        nodes_shuffled = [vertices[idx] for idx in idx_nodes]

        # hanging node is already created, should be on boundry list
        new_boundary = [hang]
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

        # connect new nodes on the boundry with inner nodes
        for vert, (node_a, node_b) in zip([vertices[0]] + nodes_shuffled, it.pairwise([new_boundary[-1]] + new_boundary)):
            node_attr = EdgeAttrs('q', False)
            nodes = (vert, node_a, node_b, node_p)
            graph.add_q_hyperedge(nodes, node_attr)

        # graph.display()
        # plt.show()
