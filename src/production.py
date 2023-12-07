import itertools as it
from copy import deepcopy
import matplotlib.pyplot as plt
import util
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph
from pprint import pprint
from utils import verify_central_hyperedges, verify_normal_edges_type


class Production:
    """ Base class for all productions """
    def __init__(self) -> None:
        pass

    def reset(self):
        """ Reset state of the production so that it can be applied again.
        Default impl does nothing."""
        pass

    def get_lhs(self) -> Graph:
        raise NotImplementedError("This method must be overrided in subclasses")

    def is_mapping_feasible(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> bool:
        """ Checks whether the production can be applied on given mapping.

        :param graph: the original 'state' graph
        :param mapping: mapping between subgraph of graph & production lhs,
        see https://networkx.org/documentation/stable/reference/algorithms/isomorphism.vf2.html#subgraph-isomorphism
        for details.

        :returns: bool is the production can be successfully applied, false if not"""
        raise NotImplementedError("This method must be overrided in subclasses")

    def apply(self, graph: Graph) -> bool:
        self.reset()
        lhs = self.get_lhs()
        for mapping in graph.generate_subgraphs_isomorphic_with(lhs):
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
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def reset(self):
        self.rev_mapping = None

    def __create_lhs(self) -> Graph:
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        nodes = [node_0, node_1, node_2, node_3]
        graph.add_node_collection(nodes)

        nodes.append(node_0)

        # Add two edges of type Q
        graph.add_edge(Edge(node_0.handle, node_2.handle, EdgeAttrs(kind='q', value=True)))
        graph.add_edge(Edge(node_1.handle, node_3.handle, EdgeAttrs(kind='q', value=True)))

        for node_0, node_1 in it.pairwise(nodes):
            graph.add_edge(Edge(node_0.handle, node_1.handle, EdgeAttrs(kind='e', value=False)))

        # graph.display()
        # plt.show()

        return graph


    def is_mapping_feasible(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> bool:
        # Now we have mapping of lhs nodes to `graph` nodes.
        self.rev_mapping = util.reverse_dict_mapping(mapping)

        # Aliasing for convenience
        rev_mapping = self.rev_mapping

        nodes = [
            graph.node_for_handle(rev_mapping[i]) for i in range(0, len(rev_mapping))
        ]

        if any(map(lambda node: node.attrs.hanging, nodes)):
            return False

        # We still need to check whether the hyperedge in the cell centre has appropriate value,
        if not verify_central_hyperedges(graph, nodes):
            return False

        # Also we need to verify all the edges are of appropriate type
        if not verify_normal_edges_type(graph, nodes):
            return False

        return True


    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        # Break the edges (1, 2), (2, 3), (3, 4), (4, 1), creating 4 new nodes
        # Add 5 new node to the center of the split
        rev_mapping = self.rev_mapping

        nodes = [
            graph.node_for_handle(rev_mapping[i]) for i in range(0, 4)
        ]

        new_nodes = []
        for node_a, node_b in it.pairwise(nodes + [nodes[0]]):
            x = (node_a.attrs.x + node_b.attrs.x) / 2
            y = (node_a.attrs.y + node_b.attrs.y) / 2
            edge_attrs = graph.edge_attrs((node_a.handle, node_b.handle))
            h = not edge_attrs.value
            new_node = Node(NodeAttrs('v', x, y, h))
            new_nodes.append(new_node)

            graph.remove_edge(node_a.handle, node_b.handle)
            graph.add_node(new_node)
            graph.add_edge(Edge(u=node_a.handle, v=new_node.handle, attrs=EdgeAttrs('e', edge_attrs.value)))
            graph.add_edge(Edge(u=new_node.handle, v=node_b.handle, attrs=EdgeAttrs('e', edge_attrs.value)))

        # the central node
        x = sum(map(lambda node: node.attrs.x, nodes)) / 4
        y = sum(map(lambda node: node.attrs.y, nodes)) / 4
        h = False
        new_node = Node(NodeAttrs('v', x, y, h))
        graph.add_node(new_node)

        for node in new_nodes:
            graph.add_edge(Edge(node.handle, new_node.handle, EdgeAttrs('e', False)))

        # add Q edges
        for node_a, node_b in zip(nodes[:2], nodes[2:]):
            graph.remove_edge(node_a.handle, node_b.handle)

        for node_a, node_b in it.pairwise(new_nodes + [new_nodes[0]]):
            graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs('q', False)))

        for old_node in nodes:
            graph.add_edge(Edge(new_node.handle, old_node.handle, EdgeAttrs('q', False)))

        graph.display()
        plt.show()


class P2(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None
        self.hanging_node: Node | None = None
        self.not_hanging_nodes: list[Node] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def reset(self):
        self.rev_mapping = None

    def __create_lhs(self) -> Graph:
        graph = Graph()

        node_0 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_1 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_2 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_3 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_4 = Node(NodeAttrs('v', 1, 0.5, True), 4)
        nodes = [node_0, node_1, node_4, node_2, node_3]

        graph.add_node_collection(nodes)

        # Add two edges of type Q
        graph.add_edge(Edge(node_0.handle, node_2.handle, EdgeAttrs(kind='q', value=True)))
        graph.add_edge(Edge(node_1.handle, node_3.handle, EdgeAttrs(kind='q', value=True)))

        for node_1, node_2 in it.pairwise(nodes + [node_0]):
            graph.add_edge(Edge(node_1.handle, node_2.handle, EdgeAttrs(kind='e', value=False)))

        # graph.display()
        # plt.show()

        return graph

    def is_mapping_feasible(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> bool:
        # Now we have mapping of lhs nodes to `graph` nodes.
        self.rev_mapping = util.reverse_dict_mapping(mapping)

        # Aliasing for convenience
        rev_mapping = self.rev_mapping

        nodes = [
            graph.node_for_handle(rev_mapping[i]) for i in rev_mapping.keys()
        ]

        filtered_hanging_nodes = list(filter(lambda node: node.attrs.hanging, nodes))
        if len(filtered_hanging_nodes) != 1:
            return False

        self.hanging_node = filtered_hanging_nodes[0]

        # Check whether the hyperedge in the cell centre has appropriate value
        not_hanging_nodes = deepcopy(nodes)
        not_hanging_nodes.remove(filtered_hanging_nodes[0])
        if not verify_central_hyperedges(graph, nodes=not_hanging_nodes):
            return False

        self.not_hanging_nodes = not_hanging_nodes

        # Verify all the edges are of appropriate type
        if not verify_normal_edges_type(graph, nodes):
            return False

        return True

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        rev_mapping = self.rev_mapping
        nodes = [
            graph.node_for_handle(rev_mapping[i]) for i in rev_mapping.keys()
        ]

        # change hanging value of hanging node
        replaced_hanging_node = Node(NodeAttrs('v', self.hanging_node.attrs.x, self.hanging_node.attrs.y, False))
        graph.add_node(replaced_hanging_node)

        new_nodes = [replaced_hanging_node]
        for node_a, node_b in it.pairwise(nodes + [nodes[0]]):
            edge_attrs = graph.edge_attrs((node_a.handle, node_b.handle))
            if node_a.attrs.hanging:
                graph.add_edge(Edge(u=replaced_hanging_node.handle, v=node_b.handle, attrs=EdgeAttrs('e', edge_attrs.value)))
            elif node_b.attrs.hanging:
                graph.add_edge(Edge(u=node_a.handle, v=replaced_hanging_node.handle, attrs=EdgeAttrs('e', edge_attrs.value)))
            else:
                x = (node_a.attrs.x + node_b.attrs.x) / 2
                y = (node_a.attrs.y + node_b.attrs.y) / 2
                h = not edge_attrs.value
                new_node = Node(NodeAttrs('v', x, y, h))
                new_nodes.append(new_node)

                graph.remove_edge(node_a.handle, node_b.handle)
                graph.add_node(new_node)
                graph.add_edge(Edge(u=node_a.handle, v=new_node.handle, attrs=EdgeAttrs('e', edge_attrs.value)))
                graph.add_edge(Edge(u=new_node.handle, v=node_b.handle, attrs=EdgeAttrs('e', edge_attrs.value)))

        # remove left hanging node
        graph.remove_node(self.hanging_node.handle)

        # the central node
        x = sum(map(lambda node: node.attrs.x, self.not_hanging_nodes)) / 4
        y = sum(map(lambda node: node.attrs.y, self.not_hanging_nodes)) / 4
        h = False
        new_node = Node(NodeAttrs('v', x, y, h))
        graph.add_node(new_node)

        for node in new_nodes:
            graph.add_edge(Edge(node.handle, new_node.handle, EdgeAttrs('e', False)))

        # TODO: add Q edges

        graph.display()
        plt.show()
