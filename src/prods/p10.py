from prods.base import *

class P10(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None

    def get_lhs(self) -> Graph:
        return self.lhs

    def reset(self):
        self.rev_mapping = None

    def __create_lhs(self) -> Graph:
        graph = util.basic_pentagon(for_lhs=True)
        # handle is 6 because the interior is 5
        graph.add_hanging_node(u=0, v=1, handle=6)
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
        node_h = graph.node_for_handle(rev_mapping[6])

        # check vertices' labels
        for node in vertices:
            if node.attrs.label != 'v' or node.attrs.hanging:
                return False

        # in case of inner node, the `hanging' parameter means that the
        # polygon is chosen to be broken; it is the same as the R parameter 
        if not node_p.attrs.hanging or node_p.attrs.label != 'p':
            return False

        if not node_h.attrs.hanging:
            return False

        # verify edges coming out of the inner node
        for node in vertices:
            edge = graph.edge_for_handles(node.handle, node_p.handle)
            if edge.attrs.kind != 'p':
                return False

        idx_nodes = [1, 4, 2, 3, 0]
        nodes_shuffled = [vertices[idx] for idx in idx_nodes]
        for node_a, node_b in it.pairwise([node_h] + nodes_shuffled + [node_h]):
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
        node_h = graph.node_for_handle(rev_mapping[6])

        # you must get edges attrs before you remove, now it is relevant
        attrs = graph.edge_attrs((vertices[0].handle, node_h.handle))
        is_boundry = attrs.value
        x = node_h.attrs.x
        y = node_h.attrs.y
        hdl = node_h.handle
        graph.remove_node(node_h.handle)
        # change hanging atribute of the node
        hang = Node(NodeAttrs('v', x, y, hanging=False), hdl)
        graph.add_node(hang)
        # recreate edges with proper boundry property
        new_attr = EdgeAttrs('e', is_boundry)
        edge = Edge(vertices[0].handle, hdl, new_attr)
        graph.add_edge(edge)
        new_attr = EdgeAttrs('e', is_boundry)
        edge = Edge(vertices[1].handle, hdl, new_attr)
        graph.add_edge(edge)

        # skip first pair because it already exists
        idx_nodes = [1, 4, 2, 3, 0]
        nodes_shuffled = [vertices[idx] for idx in idx_nodes]

        # hanging node is already created, should be on boundry list
        new_boundry = [hang]
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

        graph.remove_node(node_p.handle)

        x = node_p.attrs.x
        y = node_p.attrs.y
        central = Node(NodeAttrs('v', x, y, hanging=False), node_p.handle)
        graph.add_node(central)

        for new_node in new_boundry:
            attr = EdgeAttrs('e', False)
            edge = Edge(new_node.handle, central.handle, attr)
            graph.add_edge(edge)

        # connect new nodes on the boundry with inner nodes
        inner_nodes = []
        for vert, (node_a, node_b) in zip([vertices[0]] + nodes_shuffled, it.pairwise([new_boundry[-1]] + new_boundry)):
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
