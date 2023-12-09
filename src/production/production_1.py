import itertools as it
from copy import deepcopy
import matplotlib.pyplot as plt
import util
from typing import Dict, Optional
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node, GraphMapping
from graph import Graph
from pprint import pprint
from util import verify_central_hyperedges
from itertools import combinations
from .model import Production



class P1(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()

    def get_lhs(self) -> Graph:
        return self.lhs

    def __create_lhs(self) -> Graph:
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        nodes = [node_0, node_1, node_2, node_3]
        graph.add_node_collection(nodes)


        # Add two edges of type Q, note that they have the same handle!!!

        graph.add_q_hyperedge(nodes, EdgeAttrs('q', True), 4)

        nodes.append(node_0)

        for node_a, node_b in it.pairwise(nodes):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        # graph.display()
        # plt.show()

        return graph

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        # Break the edges (1, 2), (2, 3), (3, 4), (4, 1), creating 4 new nodes
        # Add 5 new node to the center of the split
        rev_mapping = self._rev_mapping

        v_nodes = [
            graph.node_for_handle(rev_mapping[i]) for i in range(0, 4)
        ]
        q_node = graph.node_for_handle(rev_mapping[4])

        new_border_nodes = []
        for node_a, node_b in it.pairwise(v_nodes + [v_nodes[0]]):
            x, y = util.avg_point_from_nodes((node_a, node_b))
            edge_attrs = graph.edge_attrs((node_a.handle, node_b.handle))
            h = not edge_attrs.flag
            new_node = Node(NodeAttrs('v', x, y, h)) # has no handle, will be assigned when adding to graph
            new_border_nodes.append(new_node)

            graph.remove_edge(node_a.handle, node_b.handle)
            graph.add_node(new_node)
            graph.add_edge(Edge(u=node_a.handle, v=new_node.handle, attrs=EdgeAttrs('e', edge_attrs.flag)))
            graph.add_edge(Edge(u=new_node.handle, v=node_b.handle, attrs=EdgeAttrs('e', edge_attrs.flag)))

        # the central node
        x, y = util.avg_point_from_nodes(v_nodes)
        central_node = Node(NodeAttrs('v', x, y, flag=False))
        graph.add_node(central_node)

        for node in new_border_nodes:
            graph.add_edge(Edge(node.handle, central_node.handle, EdgeAttrs('e', False)))

        # remove old Q hyperedge
        graph.remove_q_hyperedge(q_node.handle)

        # add four new Q hyperedges
        for corner_node, new_nodes in zip(v_nodes, it.pairwise([new_border_nodes[-1]] + new_border_nodes)):
            graph.add_q_hyperedge((corner_node, *new_nodes, central_node), EdgeAttrs('q', False))

        # graph.display()
        # plt.show()
