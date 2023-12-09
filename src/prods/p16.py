from prods.base import *

class P16(Production):
    def __init__(self, idx=None) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None
        self.idx: NodeHandle = idx

    def get_lhs(self) -> Graph:
        return self.lhs

    def reset(self):
        self.rev_mapping = None

    def __create_lhs(self) -> Graph:
        graph, _ = util.basic_star5(for_lhs=True)
        return graph

    def is_mapping_feasible(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> bool:
        # Now we have mapping of lhs nodes to `graph` nodes.
        self.rev_mapping = util.reverse_dict_mapping(mapping)

        # Aliasing for convenience
        rev_mapping = self.rev_mapping

        # get square's vertices
        vertices = [
            graph.node_for_handle(rev_mapping[i]) for i in range(0, 5)
        ]
        # get inner node, the hyperedge
        node_p = graph.node_for_handle(rev_mapping[5])

        # check if we found chosen node
        # if none of the idices were given, then pick up any star
        if self.idx is not None:
            if node_p.handle != self.idx:
                return False
 
        # check vertices' labels
        for node in vertices:
            if node.attrs.label != 'v':
                return False

        # in case of inner node, the `hanging' parameter means that the
        # polygon is chosen to be broken; it is the same as the R parameter 
        if node_p.attrs.hanging or node_p.attrs.label != 'p':
            return False

        # verify edges coming out of the inner node
        for node in vertices:
            edge = graph.edge_for_handles(node.handle, node_p.handle)
            if edge.attrs.kind != 'p':
                return False

        return True

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
        x = node_p.attrs.x
        y = node_p.attrs.y

        graph.remove_node(node_p.handle)
        new_p = Node(NodeAttrs('p', x, y, hanging=True), node_p.handle)
        graph.add_node(new_p)
        for node in vertices:
            attr = EdgeAttrs('p', value=True)
            edge = Edge(node.handle, new_p.handle, attr)
            graph.add_edge(edge)

        graph.display()
        plt.show()
