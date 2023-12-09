from prods.base import *

class P2(Production):
    def __init__(self) -> None:
        self.lhs: Graph = self.__create_lhs()
        self.rev_mapping: Dict[NodeHandle, NodeHandle] | None = None
        self.hanging_node: Node | None = None
        self.external_nodes: list[Node] | None = None

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
            graph.node_for_handle(rev_mapping[i]) for i in (0, 1, 4, 2, 3, 0)
        ]

        # check if appropriate vertex in the middle of the edge is hanging
        if not nodes[2].attrs.hanging:
            return False
        for i in (0, 1, 3, 4):
            if nodes[i].attrs.hanging:
                return False

        self.hanging_node = nodes[2]
        external_nodes = deepcopy(nodes[:-1])
        external_nodes.remove(self.hanging_node)
        self.external_nodes = external_nodes

        # Check whether the hyperedge in the cell centre has appropriate value
        if not verify_central_hyperedges(graph, nodes=self.external_nodes):
            return False

        # Verify all the edges are of appropriate type
        for node_a, node_b in it.pairwise(nodes):
            edge = graph.edge_for_handles(node_a.handle, node_b.handle)
            if edge.attrs.kind != 'e':
                return False

        return True

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]):
        rev_mapping = self.rev_mapping
        nodes = [
            graph.node_for_handle(rev_mapping[i]) for i in (0, 1, 4, 2, 3, 0)
        ]

        # change hanging value of hanging node
        replaced_hanging_node = Node(NodeAttrs('v', self.hanging_node.attrs.x, self.hanging_node.attrs.y, False))
        graph.add_node(replaced_hanging_node)

        new_nodes = [replaced_hanging_node]
        for node_a, node_b in it.pairwise(nodes):
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
        x = sum(map(lambda node: node.attrs.x, self.external_nodes)) / 4
        y = sum(map(lambda node: node.attrs.y, self.external_nodes)) / 4
        h = False
        new_node = Node(NodeAttrs('v', x, y, h))
        graph.add_node(new_node)

        for node in new_nodes:
            graph.add_edge(Edge(node.handle, new_node.handle, EdgeAttrs('e', False)))

        # # add Q edges
        for node_a, node_b in zip(self.external_nodes[:2], self.external_nodes[2:]):
            graph.remove_edge(node_a.handle, node_b.handle)

        for old_node in self.external_nodes:
            graph.add_edge(Edge(new_node.handle, old_node.handle, EdgeAttrs('q', False)))

        paired_nodes: list[tuple[Node, Node]] = []
        for i in range(len(new_nodes)):
            for j in range(i + 1, len(new_nodes)):
                # Check if the x or y value of the nodes are different
                if new_nodes[i].attrs.x != new_nodes[j].attrs.x and \
                        new_nodes[i].attrs.y != new_nodes[j].attrs.y:
                    paired_nodes.append((new_nodes[i], new_nodes[j],))

        for pair in paired_nodes:
            graph.add_edge(Edge(pair[0].handle, pair[1].handle, EdgeAttrs('q', False)))

        graph.display()
        plt.show()

