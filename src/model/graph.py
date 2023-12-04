import networkx as nx
from typing import Iterable, Optional, Dict, Any
from .point import Point
from .node import Node

EdgeAttributes = Dict[Any, Any]
EdgeType = tuple[Node, Node] | tuple[Node, Node, EdgeAttributes]

class Graph:
    def __init__(self) -> None:
        self._graph = nx.Graph()

    def __contains__(self, node: Node) -> bool:
        return self._graph.has_node(node)

    def add_node(self, node: Node):
        self._graph.add_node(node)

    def add_node_collection(self, node_collection: Iterable[Node]):
        for node in node_collection:
            self.add_node(node)

    def remove_node(self, node: Node):
        self._graph.remove_node(node)

    def remove_node_collection(self, node_collection: Iterable[Node]):
        for node in node_collection:
            self.remove_node(node)

    def add_edge(self, u_of_edge: Node, v_of_edge: Node, attrs: EdgeAttributes = None):
        self._graph.add_edge(u_of_edge=u_of_edge, v_of_edge=v_of_edge, value="err")

    def add_edge_collection(self, edge_collection: Iterable[EdgeType]):
        for edge in edge_collection:
            self.add_edge(*edge)
            # self.add_edge(edge[0], edge[1], **edge[2] if len(edge) > 2 else None)

    def remove_edge(self, node_1: Node, node_2: Node):
        self._graph.remove_edge(node_1, node_2)

    def remove_edge_collection(self, edge_collection: Iterable[EdgeType]):
        for edge in edge_collection:
            self.remove_edge(edge)

    def generate_subgraphs_isomorphic_with(self, other: 'Graph') -> Iterable[Any]:
        pass

    def backing_graph(self) -> nx.Graph:
        return self._graph