import networkx as nx
from typing import Iterable, Optional, Dict, Any, Hashable, NamedTuple

Node = int

class NodeAttrs(NamedTuple):
    label: str
    x: float
    y: float

EdgeAttrs = Dict[Any, Any]
EdgeType = tuple[NodeAttrs, NodeAttrs] | tuple[NodeAttrs, NodeAttrs, EdgeAttrs]

class Graph:
    def __init__(self) -> None:
        self._graph = nx.Graph()

    def __contains__(self, node: Node) -> bool:
        return self._graph.has_node(node)

    def add_node(self, node: Hashable, attrs: Optional[NodeAttrs]):
        self._graph.add_node(node, payload=attrs)

    def add_node_collection(self, node_collection: Iterable[tuple[Node, NodeAttrs]]):
        for node, attrs in node_collection:
            self.add_node(node, attrs)

    def remove_node(self, node: Node):
        self._graph.remove_node(node)

    def remove_node_collection(self, node_collection: Iterable[Node]):
        for node in node_collection:
            self.remove_node(node)

    def add_edge(self, u_of_edge: Node, v_of_edge: Node, attrs: Optional[EdgeAttrs] = None):
        self._graph.add_edge(u_of_edge=u_of_edge, v_of_edge=v_of_edge, payload=attrs)

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
        gm = nx.isomorphism.GraphMatcher(self._graph, other.nx_graph)
        return gm.subgraph_isomorphisms_iter()

    def __getitem__(self, node: Node) -> NodeAttrs:
        # Actually we want to throw in case there is no such node
        return self._graph.nodes[node]['payload']

    def display(self, **kwargs):
        positions = {
            node: (self[node].x, self[node].y) for node in self._graph.nodes
        }
        edge_labels = {
            (u, v): f'u <-> v' for u, v in self._graph.edges
        }
        node_labels = {
            u: f'{u}\n{self[u].label}, x={self[u].x}, y={self[u].y}' for u in self._graph.nodes
        }

        nx.draw_networkx(self.nx_graph, pos=positions, labels=node_labels, **kwargs)
        nx.draw_networkx_edge_labels(self.nx_graph, pos=positions, edge_labels=edge_labels, **kwargs)


    @property
    def nx_graph(self) -> nx.Graph:
        return self._graph