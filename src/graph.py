import itertools as it
import networkx as nx
from model import (
    Node, NodeHandle,
    NodeAttrs, Edge,
    EdgeAttrs, GraphMapping,
    EdgeEndpoints
)
from typing import Optional, Iterable, Any, Callable
import util


def node_equality(nx_node_attrs_1, nx_node_attrs_2) -> bool:
    attrs_1: NodeAttrs = nx_node_attrs_1['payload']
    attrs_2: NodeAttrs = nx_node_attrs_2['payload']

    return (
        attrs_1.label == attrs_2.label and
        attrs_1.flag == attrs_2.flag
    )


def edge_equality(nx_edge_attrs_1, nx_edge_attrs_2) -> bool:
    attrs_1: EdgeAttrs = nx_edge_attrs_1['payload']
    attrs_2: EdgeAttrs = nx_edge_attrs_2['payload']

    return (
        attrs_1.kind == attrs_2.kind and
        attrs_2.flag == attrs_2.flag
    )


class Graph:
    def __init__(self) -> None:
        self._graph = nx.Graph()
        self._node_handle_factory = it.count().__next__

    def __contains__(self, node: NodeHandle) -> bool:
        return self._graph.has_node(node)

    def add_node(self, node: Node) -> NodeHandle:
        """ IMPORTANT:
        If the node.handle == None the we generate graph-wide-unique handle here
        """
        if node.handle is None:
            node.handle = self._node_handle_factory()
        self._graph.add_node(node.handle, payload=node.attrs)
        return node.handle

    def add_node_collection(self, node_collection: Iterable[Node]) -> Iterable[NodeHandle]:
        return [self.add_node(node) for node in node_collection]

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

    def remove_edge_with_endpoints(self, edge: EdgeEndpoints):
        # Leaving method `remove_edge` to avoid refactorings & keeping backward compat
        self._graph.remove_edge(edge[0], edge[1])

    def remove_edge_collection(self, edge_collection: Iterable[Edge]):
        for edge in edge_collection:
            self.remove_edge(edge.u, edge.v)

    def generate_subgraphs_isomorphic_with(self, other: 'Graph') -> Iterable[GraphMapping]:
        gm = nx.isomorphism.GraphMatcher(self._graph, other.nx_graph, node_match=node_equality, edge_match=edge_equality)
        return gm.subgraph_isomorphisms_iter()

    def generate_subgraphs_monomorphic_with(self, other: 'Graph') -> Iterable[GraphMapping]:
        gm = nx.isomorphism.GraphMatcher(self._graph, other.nx_graph, node_match=node_equality, edge_match=edge_equality)
        return gm.subgraph_monomorphisms_iter()


    def node_for_handle(self, handle: NodeHandle) -> Node:
        return Node(handle=handle, attrs=self[handle])

    def __getitem__(self, node: NodeHandle) -> NodeAttrs:
        # Actually we want to throw in case there is no such node
        try:
            return self._graph.nodes[node]['payload']
        except KeyError as err:
            print(f"Attempt to get node with handle {node} that does not exist in graph")
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


    def add_q_hyperedge(self, nodes: tuple[Node, Node, Node, Node], edge_attrs: EdgeAttrs, q_node_handle: NodeHandle = None):
        assert len(nodes) == 4
        assert edge_attrs.kind == 'q'
        x, y = util.avg_point_from_nodes(nodes)
        node_attrs = NodeAttrs('q', x, y, edge_attrs.flag)
        q_node = Node(node_attrs, q_node_handle)
        self.add_node(q_node)
        self.add_edge_collection(Edge(node.handle, q_node.handle, edge_attrs) for node in nodes)

    def remove_q_hyperedge(self, q_node_handle: NodeHandle):
        """ Remove Q hyperedge with given (hyper)node in the centre.
        This method removes also all Q-edges.
        """
        q_node_attrs = self.node_attrs(q_node_handle)
        assert q_node_attrs.label == 'q', f"Attempt to remove q hyperedge with handle for node with attrs {q_node_attrs}, label={q_node_attrs.label}"
        self.remove_node(q_node_handle)

    def add_p_hyperedge(self, nodes: tuple[Node, Node, Node, Node, Node], edge_attrs: EdgeAttrs, p_node_handle: NodeHandle = None, p_node_coords: tuple[float, float] = None):
        """ Add P-hyperedge to the graph.

        :param nodes: tuple/list of FIVE nodes, that the P-hyperedge should connect; ORDER OF THE NODES MATTERS FOR THE LAYOUT, see below
        :param edge_attrs: shared attributes for all the edges that the hyperedge is comprised of
        :param p_node_handle: optional node handle for the P-hypernode; if not specified an graph-unique id will be assigned automatically
        :param p_node_coords: optional tuple with coordinates for the P-hypernode; if not specified the position will be calculated as mean point between: nodes[0], nodes[1], nodes[3], nodes[4]
        """

        assert len(nodes) == 5
        assert edge_attrs.kind == 'p'
        x, y = p_node_coords if p_node_coords is not None else util.avg_point_from_nodes((nodes[0], nodes[1], nodes[3], nodes[4]))
        node_attrs = NodeAttrs('p', x, y, edge_attrs.flag)
        p_node = Node(node_attrs, handle=p_node_handle)
        self.add_node(p_node)
        self.add_edge_collection(Edge(node.handle, p_node.handle, edge_attrs) for node in nodes)


    def remove_p_hyperedge(self, p_node_handle: NodeHandle):
        """ Remove P hyperedge with given (hyper)node in the centre.
        This method removes also all P-edges.
        """
        p_node_attrs = self.node_attrs(p_node_handle)
        assert p_node_attrs.label == 'p', f"Attempt to remove P hyperedge with handle for node with attrs {p_node_attrs}, label={p_node_attrs.label}"
        self.remove_node(p_node_handle)


    def split_edge_with_vnode(self, edge: EdgeEndpoints, node_flag: bool = None, node_handle: NodeHandle = None) -> Node:
        """ Splits given edge with new 'v' node.

        :param edge: endpoints of the to-be-splitted edge
        :param node_flag: optional flag for the new node; if not specified it will default to negated flag value of the edge that is being split
                          as it is required in most of the productions
        :param node_handle: optional handle for the new node; if not specified an graph-unique id will be assigned automatically
        :return: newly created node
        """
        attrs_u = self.node_attrs(edge[0])
        attrs_v = self.node_attrs(edge[1])
        x, y = util.avg_point_from_node_attrs((attrs_u, attrs_v))
        edge_attrs = self.edge_attrs(edge)

        hanging = node_flag if node_flag is not None else not edge_attrs.flag

        h_node = Node(NodeAttrs('v', x, y, flag=hanging), handle=node_handle)

        self.remove_edge_with_endpoints(edge)
        self.add_node(h_node)
        self.add_edge(Edge(edge[0], h_node.handle, EdgeAttrs(kind='e', flag=edge_attrs.flag)))
        self.add_edge(Edge(h_node.handle, edge[1], EdgeAttrs(kind='e', flag=edge_attrs.flag)))

        return h_node


    @property
    def nx_graph(self) -> nx.Graph:
        return self._graph

    @property
    def node_handle_factory(self) -> Callable[[], int]:
        return self._node_handle_factory
