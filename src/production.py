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



class Production:
    """ Base class for all productions """
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        """ Reset state of the production so that it can be applied again. """
        self._rev_mapping = None

    def get_lhs(self) -> Graph:
        raise NotImplementedError("This method must be overrided in subclasses")

    def is_mapping_feasible(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> bool:
        """ Checks whether the production can be applied on given mapping.

        :param graph: the original 'state' graph
        :param mapping: mapping between subgraph of graph & production lhs,
        see https://networkx.org/documentation/stable/reference/algorithms/isomorphism.vf2.html#subgraph-isomorphism
        for details.

        :returns: bool is the production can be successfully applied, false if not"""
        return True
        # raise NotImplementedError("This method must be overrided in subclasses")

    def apply(self, graph: Graph) -> bool:
        self.reset()
        lhs = self.get_lhs()
        for mapping in graph.generate_subgraphs_isomorphic_with(lhs):
            self._rev_mapping = util.reverse_dict_mapping(mapping)
            if self.is_mapping_feasible(graph, mapping):
                self.apply_with_mapping(graph, mapping)
                return True
        return False

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> None:
        """ Implement the production by overriding this method.
        This method should mutate the graph passed as argument.

        :param graph: the original 'state' graph
        :param mapping: mapping between subgraph of graph & production lhs,
        see https://networkx.org/documentation/stable/reference/algorithms/isomorphism.vf2.html#subgraph-isomorphism
        for details.

        Please note that this method is called only if `is_mapping_feasible` returned True for `mapping`."""
        raise NotImplementedError("This method must be overrided in subclasses")

    def __call__(self, graph: Graph) -> bool:
        return self.apply(graph)

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


        graph.display()
        plt.show()

        return graph


    # def is_mapping_feasible(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> bool:
    #     # Now we have mapping of lhs nodes to `graph` nodes.
    #     # Aliasing for convenience
    #     rev_mapping = self._rev_mapping
    #
    #     v_nodes = [
    #         graph.node_for_handle(rev_mapping[i]) for i in range(0, len(rev_mapping) - 1)
    #     ]
    #     q_node = graph.node_for_handle(rev_mapping[len(rev_mapping) - 1])
    #
    #     if any(map(lambda node: node.attrs.flag, v_nodes)):
    #         print('Rejecting because of bad hanging node value')
    #         return False
    #
    #     # We still need to check whether the hyperedge in the cell centre has appropriate value,
    #     if q_node.attrs.label != 'q' or q_node.attrs.flag == False:
    #         print('Rejecting because of q', q_node)
    #         print(rev_mapping)
    #         return False
    #
    #     # Also we need to verify all the edges are of appropriate type
    #     for node_a, node_b in it.pairwise(v_nodes + [v_nodes[0]]):
    #         edge = graph.edge_for_handles(node_a.handle, node_b.handle)
    #         if edge.attrs.kind != 'e':
    #             print('Rejecting because e edge')
    #             return False
    #
    #     return True


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

        graph.display()
        plt.show()


class P2(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.hanging_node: Node | None = None
        self.external_nodes: list[Node] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def __create_lhs(self) -> Graph:
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 1, 0.5, True), 4)
        nodes = [node_0, node_1, node_4, node_2, node_3]
        corner_nodes = (node_0, node_1, node_2, node_3)

        graph.add_node_collection(nodes)

        graph.add_q_hyperedge(corner_nodes, EdgeAttrs('q', True), 5)

        for node_a, node_b in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs(kind='e', flag=False)))

        # graph.display()
        # plt.show()

        return graph

    # def is_mapping_feasible(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> bool:
    #     # Now we have mapping of lhs nodes to `graph` nodes.
    #
    #     # Aliasing for convenience
    #     rev_mapping = self._rev_mapping
    #
    #     nodes = [
    #         graph.node_for_handle(rev_mapping[i]) for i in (0, 1, 4, 2, 3, 0)
    #     ]
    #
    #     # check if appropriate vertex in the middle of the edge is hanging
    #     if not nodes[2].attrs.flag:
    #         return False
    #     for i in (0, 1, 3, 4):
    #         if nodes[i].attrs.flag:
    #             return False
    #
    #     self.hanging_node = nodes[2]
    #     external_nodes = deepcopy(nodes[:-1])
    #     external_nodes.remove(self.hanging_node)
    #     self.external_nodes = external_nodes
    #
    #     # Check whether the hyperedge in the cell centre has appropriate value
    #     if not verify_central_hyperedges(graph, nodes=self.external_nodes):
    #         return False
    #
    #     # Verify all the edges are of appropriate type
    #     for node_a, node_b in it.pairwise(nodes):
    #         edge = graph.edge_for_handles(node_a.handle, node_b.handle)
    #         if edge.attrs.kind != 'e':
    #             return False
    #
    #     return True

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        rev_mapping = self._rev_mapping

        # counter-clock-wise
        in_order_nodes = [graph.node_for_handle(rev_mapping[i]) for i in (0, 1, 2, 3, 4, 5)]
        corner_nodes = [node for node in in_order_nodes[:-2]]
        v_nodes = [
            graph.node_for_handle(rev_mapping[i]) for i in (0, 1, 4, 2, 3, 0)
        ]
        hanging_node = graph.node_for_handle(rev_mapping[4])
        q_node = graph.node_for_handle(rev_mapping[5])

        # change hanging value of hanging node
        # we actualy have reference to this node, so we can modify it in place
        hanging_node.attrs.flag = False

        new_border_nodes = []
        for node_a, node_b in ((in_order_nodes[0], in_order_nodes[1]), (in_order_nodes[2], in_order_nodes[3]), (in_order_nodes[3], in_order_nodes[0])):
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
        # the central node
        x, y = util.avg_point_from_nodes(corner_nodes)
        central_node = Node(NodeAttrs('v', x, y, flag=False))
        graph.add_node(central_node)

        for node in new_border_nodes + [hanging_node]:
            graph.add_edge(Edge(node.handle, central_node.handle, EdgeAttrs('e', False)))

        graph.remove_q_hyperedge(q_node.handle)

        # # add Q edges
        assert len(new_border_nodes) == 3
        new_border_nodes.insert(1, hanging_node)

        for corner_node, new_nodes in zip(corner_nodes, it.pairwise([new_border_nodes[-1]] + new_border_nodes)):
            graph.add_q_hyperedge((corner_node, *new_nodes, central_node), EdgeAttrs('q', False))

        # for node_a, node_b in zip(self.external_nodes[:2], self.external_nodes[2:]):
        #     graph.remove_edge(node_a.handle, node_b.handle)
        #
        # q_edge_handles = []
        # for old_node in self.external_nodes:
        #     edge = Edge(new_node.handle, old_node.handle, EdgeAttrs('q', False))
        #     graph.add_edge(edge)
        #     q_edge_handles.append(edge.attrs.handle)
        #
        # new_nodes[0], new_nodes[1] = new_nodes[1], new_nodes[0]
        # for (node_a, node_b), handle in zip(it.pairwise([new_nodes[-1]] + new_nodes), q_edge_handles):
        #     graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs('q', False, handle)))

        graph.display()
        plt.show()
