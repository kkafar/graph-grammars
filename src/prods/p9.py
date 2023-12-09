from prods.base import *

class P9(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def reset(self):
        self.rev_mapping = None

    def __create_lhs(self) -> Graph:
        return util.basic_pentagon(for_lhs=True)

    # check whether found monomorphism has correct labels
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
        idx_nodes = [0, 1, 4, 2, 3, 0]
        nodes_shuffled = [vertices[idx] for idx in idx_nodes]

        # check vertices' labels
        for node in vertices:
            if node.attrs.label != 'v' or node.attrs.hanging:
                return False

        # in case of inner node, the `hanging' attribute means that the
        # polygon is chosen to be broken; it is the same as the R parameter 
        if not node_p.attrs.hanging or node_p.attrs.label != 'p':
            return False

        # verify edges coming out of the inner node
        for node in vertices:
            edge = graph.edge_for_handles(node.handle, node_p.handle)
            if edge.attrs.kind != 'p':
                return False

        for node_a, node_b in it.pairwise(nodes_shuffled):
            edge = graph.edge_for_handles(node_a.handle, node_b.handle)
            if edge.attrs.kind != 'e':
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
        idx_nodes = [0, 1, 4, 2, 3, 0]
        nodes_shuffled = [vertices[idx] for idx in idx_nodes]

        new_boundry = []
        for node_a, node_b in it.pairwise(nodes_shuffled):
            x = (node_a.attrs.x + node_b.attrs.x) / 2
            y = (node_a.attrs.y + node_b.attrs.y) / 2
            edge_attrs = graph.edge_attrs((node_a.handle, node_b.handle))
            hanging = not edge_attrs.value
            new_node = Node(NodeAttrs('v', x, y, hanging))
            new_boundry.append(new_node)

            graph.remove_edge(node_a.handle, node_b.handle)
            graph.add_node(new_node)

            new_attrs = EdgeAttrs('e', edge_attrs.value)
            edge = Edge(u=node_a.handle, v=new_node.handle, attrs=new_attrs)
            graph.add_edge(edge)
            new_attrs = EdgeAttrs('e', edge_attrs.value)
            edge = Edge(u=new_node.handle, v=node_b.handle, attrs=new_attrs)
            graph.add_edge(edge)

        # remove node with all it's edges
        graph.remove_node(node_p.handle)

        x = node_p.attrs.x
        y = node_p.attrs.y
        central = Node(NodeAttrs('v', x, y, hanging=False), node_p.handle)
        graph.add_node(central)

        for new_node in new_boundry:
            attr = EdgeAttrs('e', False)
            edge = Edge(new_node.handle, central.handle, attr)
            graph.add_edge(edge)

        # create inner nodes and connect new nodes on the boundry with inner nodes
        inner_nodes = []
        for vert, (node_a, node_b) in zip(nodes_shuffled, it.pairwise([new_boundry[-1]] + new_boundry)):
            x = (vert.attrs.x + node_a.attrs.x + node_b.attrs.x + node_p.attrs.x) / 4
            y = (vert.attrs.y + node_a.attrs.y + node_b.attrs.y + node_p.attrs.y) / 4
            inner_node = Node(NodeAttrs('q', x, y, hanging=False))
            inner_nodes.append(inner_node)
            graph.add_node(inner_node)
            attr = EdgeAttrs('q', False)
            edge = Edge(node_a.handle, inner_node.handle, attr)
            graph.add_edge(edge)
            attr = EdgeAttrs('q', False)
            edge = Edge(node_b.handle, inner_node.handle, attr)
            graph.add_edge(edge)
            attr = EdgeAttrs('q', False)
            edge = Edge(node_p.handle, inner_node.handle, attr)
            graph.add_edge(edge)
            attr = EdgeAttrs('q', False)
            edge = Edge(vert.handle, inner_node.handle, attr)
            graph.add_edge(edge)

        graph.display()
        plt.show()
