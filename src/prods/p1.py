from prods.base import *

class P1(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def reset(self):
        self.rev_mapping = None

    def __create_lhs(self) -> Graph:
        return util.basic_square(for_lhs=True)

    # check whether found isomorphism has all correct labels
    def is_mapping_feasible(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> bool:
        # Now we have mapping of lhs nodes to `graph` nodes.
        self.rev_mapping = util.reverse_dict_mapping(mapping)

        # Aliasing for convenience
        rev_mapping = self.rev_mapping

        # get square's vertices
        vertices = [
            graph.node_for_handle(rev_mapping[i]) for i in range(0, 4)
        ]
        # get inner node, the hyperedge
        node_q = graph.node_for_handle(rev_mapping[4])
 
        # check vertices' labels
        for node in vertices:
            if node.attrs.hanging or node.attrs.label != 'v':
                return False

        # in case of inner node, the `hanging' parameter means that the
        # polygon is chosen to be broken; it is the same as the R parameter 
        if not node_q.attrs.hanging or node_q.attrs.label != 'q':
            return False

        # Also we need to verify all the edges are of appropriate type
        for node_a, node_b in it.pairwise(vertices + [vertices[0]]):
            edge = graph.edge_for_handles(node_a.handle, node_b.handle)
            if edge.attrs.kind != 'e':
                return False

        # verify edges coming out of the inner node
        for node in vertices:
            edge = graph.edge_for_handles(node.handle, node_q.handle)
            if edge.attrs.kind != 'q':
                return False

        return True

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        # Break the edges (1, 2), (2, 3), (3, 4), (4, 1), creating 4 new nodes
        # Add 5 new node to the center of the split
        rev_mapping = self.rev_mapping

        vertices = [
            graph.node_for_handle(rev_mapping[i]) for i in range(0, 4)
        ]
        node_q = graph.node_for_handle(rev_mapping[4])

        new_boundry = []
        for node_a, node_b in it.pairwise(vertices + [vertices[0]]):
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
        graph.remove_node(node_q.handle)

        x = node_q.attrs.x
        y = node_q.attrs.y
        central = Node(NodeAttrs('v', x, y, hanging=False), node_q.handle)
        graph.add_node(central)

        for new_node in new_boundry:
            attr = EdgeAttrs('e', False)
            edge = Edge(new_node.handle, central.handle, attr)
            graph.add_edge(edge)

        # connect new nodes on the boundry with inner nodes
        inner_nodes = []
        for node_a, node_b in it.pairwise([new_boundry[-1]] + new_boundry):
            x = (node_a.attrs.x + node_b.attrs.x) / 2
            y = (node_a.attrs.y + node_b.attrs.y) / 2
            inner_node = Node(NodeAttrs('q', x, y, hanging=False))
            inner_nodes.append(inner_node)
            graph.add_node(inner_node)
            attr = EdgeAttrs('q', False)
            edge = Edge(node_a.handle, inner_node.handle, attr)
            graph.add_edge(edge)
            attr = EdgeAttrs('q', False)
            edge = Edge(inner_node.handle, node_b.handle, attr)
            graph.add_edge(edge)

        # connect vertices with inner nodes
        for node, inner_node in zip(vertices, inner_nodes):
            attr = EdgeAttrs('q', False)
            edge = Edge(node.handle, inner_node.handle, attr)
            graph.add_edge(edge)

        # connect inner nodes with central node
        for inner_node in inner_nodes:
            attr = EdgeAttrs('q', False)
            edge = Edge(central.handle, inner_node.handle, attr)
            graph.add_edge(edge)
            
        graph.display()
        plt.show()
