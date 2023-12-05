import networkx as nx
from typing import Iterable, Optional, Dict, Any
from .point import Point
from .node import NodeAttrs

EdgeAttrs = Dict[Any, Any]
EdgeType = tuple[NodeAttrs, NodeAttrs] | tuple[NodeAttrs, NodeAttrs, EdgeAttrs]

class Graph:
    def __init__(self) -> None:
        self._graph = nx.Graph()

    def __contains__(self, node: NodeAttrs) -> bool:
        return self._graph.has_node(node)

    def add_node(self, node: NodeAttrs):
        self._graph.add_node(node)

    def add_node_collection(self, node_collection: Iterable[NodeAttrs]):
        for node in node_collection:
            self.add_node(node)

    def remove_node(self, node: NodeAttrs):
        self._graph.remove_node(node)

    def remove_node_collection(self, node_collection: Iterable[NodeAttrs]):
        for node in node_collection:
            self.remove_node(node)

    def add_edge(self, u_of_edge: NodeAttrs, v_of_edge: NodeAttrs, attrs: EdgeAttrs = None):
        self._graph.add_edge(u_of_edge=u_of_edge, v_of_edge=v_of_edge, value="err")

    def add_edge_collection(self, edge_collection: Iterable[EdgeType]):
        for edge in edge_collection:
            self.add_edge(*edge)
            # self.add_edge(edge[0], edge[1], **edge[2] if len(edge) > 2 else None)

    def remove_edge(self, node_1: NodeAttrs, node_2: NodeAttrs):
        self._graph.remove_edge(node_1, node_2)

    def remove_edge_collection(self, edge_collection: Iterable[EdgeType]):
        for edge in edge_collection:
            self.remove_edge(edge)

    def generate_subgraphs_isomorphic_with(self, other: 'Graph') -> Iterable[Any]:
        gm = nx.isomorphism.GraphMatcher(self._graph, other.backing_graph())
        return gm.subgraph_isomorphisms_iter()

    def backing_graph(self) -> nx.Graph:
        return self._graph