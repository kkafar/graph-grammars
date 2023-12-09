import networkx as nx
from model import (
    Node, NodeHandle,
    NodeAttrs, Edge,
    EdgeAttrs, GraphMapping,
    EdgeEndpoints
)
from typing import Optional, Iterable, Any

class Graph:
    def __init__(self) -> None:
        self._graph = nx.Graph()

    def __contains__(self, node: NodeHandle) -> bool:
        return self._graph.has_node(node)

    def add_node(self, node: Node):
        self._graph.add_node(node.handle, payload=node.attrs)

    def add_node_collection(self, node_collection: Iterable[Node]):
        for node in node_collection:
            self.add_node(node)

    def remove_node(self, handle: NodeHandle):
        self._graph.remove_node(handle)

    def remove_node_collection(self, node_collection: Iterable[NodeHandle]):
        for node in node_collection:
            self.remove_node(node)

    def add_edge(self, edge: Edge):
        self._graph.add_edge(u_of_edge=edge.u, v_of_edge=edge.v, payload=edge.attrs)

    def add_edge_collection(self, edge_collection: Iterable[Edge]):
        for edge in edge_collection:
            self.add_edge(edge)

    def remove_edge(self, handle_1: NodeHandle, handle_2: NodeHandle):
        self._graph.remove_edge(handle_1, handle_2)

    def remove_edge_collection(self, edge_collection: Iterable[Edge]):
        for edge in edge_collection:
            self.remove_edge(edge.u, edge.v)

    def generate_subgraphs_isomorphic_with(self, other: 'Graph') -> Iterable[GraphMapping]:
        gm = nx.isomorphism.GraphMatcher(self._graph, other.nx_graph)
        return gm.subgraph_isomorphisms_iter()

    def node_for_handle(self, handle: NodeHandle) -> Node:
        return Node(handle=handle, attrs=self[handle])

    def __getitem__(self, node: NodeHandle) -> NodeAttrs:
        # Actually we want to throw in case there is no such node
        try:
            return self._graph.nodes[node]['payload']
        except KeyError as err:
            print(f"KEYERROR for {node}", self._graph.nodes)
            raise err

    def node_attrs(self, node: NodeHandle) -> NodeAttrs:
        return self[node]

    def edge_attrs(self, edge: EdgeEndpoints) -> EdgeAttrs:
        return self._graph[edge[0]][edge[1]]['payload']

    def edge_for_handles(self, handle_1: NodeHandle, handle_2: NodeHandle) -> Edge:
        attrs = self.edge_attrs((handle_1, handle_2))
        return Edge(handle_1, handle_2, attrs)


    def display(self, **kwargs):
        positions = {
            node: (self[node].x, self[node].y) for node in self._graph.nodes
        }
        edge_labels = {
            (u, v): f'{self.edge_attrs((u, v))}' for u, v in self._graph.edges
        }
        node_labels = {
            u: self.node_attrs(u).__str__(u) for u in self._graph.nodes
        }

        nx.draw_networkx(self.nx_graph, pos=positions, labels=node_labels, **kwargs)
        nx.draw_networkx_edge_labels(self.nx_graph, pos=positions, edge_labels=edge_labels, **kwargs)

    @property
    def nx_graph(self) -> nx.Graph:
        return self._graph
