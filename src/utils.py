import itertools as it
from typing import Dict
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
from graph import Graph


def verify_central_hyperedges(graph: 'Graph', nodes: list[Node]):
    edge_1_3 = graph.edge_for_handles(nodes[0].handle, nodes[2].handle)
    if edge_1_3.attrs.kind != 'q' or edge_1_3.attrs.value is False:
        return False

    edge_2_4 = graph.edge_for_handles(nodes[1].handle, nodes[3].handle)
    if edge_2_4.attrs.kind != 'q' or edge_2_4.attrs.value is False:
        return False
    return True


def verify_normal_edges_type(graph: 'Graph', nodes: list[Node]):
    for node_a, node_b in it.pairwise(nodes + [nodes[0]]):
        print(node_a, node_b)
        edge = graph.edge_for_handles(node_a.handle, node_b.handle)
        if edge.attrs.kind != 'e':
            return False
    return True


def break_the_quadrangle(graph: Graph, rev_mapping: Dict[NodeHandle, NodeHandle]):
    nodes = [
        graph.node_for_handle(rev_mapping[i]) for i in range(0, 4)
    ]

    new_nodes = []
    for node_a, node_b in it.pairwise(nodes + [nodes[0]]):
        x = (node_a.attrs.x + node_b.attrs.x) / 2
        y = (node_a.attrs.y + node_b.attrs.y) / 2
        edge_attrs = graph.edge_attrs((node_a.handle, node_b.handle))
        h = not edge_attrs.value
        new_node = Node(NodeAttrs('v', x, y, h))
        new_nodes.append(new_node)

        graph.remove_edge(node_a.handle, node_b.handle)
        graph.add_node(new_node)
        graph.add_edge(Edge(u=node_a.handle, v=new_node.handle, attrs=EdgeAttrs('e', edge_attrs.value)))
        graph.add_edge(Edge(u=new_node.handle, v=node_b.handle, attrs=EdgeAttrs('e', edge_attrs.value)))

    # the central node
    x = sum(map(lambda node: node.attrs.x, nodes)) / 4
    y = sum(map(lambda node: node.attrs.y, nodes)) / 4
    h = False
    new_node = Node(NodeAttrs('v', x, y, h))
    graph.add_node(new_node)

    for node in new_nodes:
        graph.add_edge(Edge(node.handle, new_node.handle, EdgeAttrs('e', False)))

    # add Q edges
    for node_a, node_b in zip(nodes[:2], nodes[2:]):
        graph.remove_edge(node_a.handle, node_b.handle)

    for node_a, node_b in it.pairwise(new_nodes + [new_nodes[0]]):
        graph.add_edge(Edge(node_a.handle, node_b.handle, EdgeAttrs('q', False)))

    for old_node in nodes:
        graph.add_edge(Edge(new_node.handle, old_node.handle, EdgeAttrs('q', False)))
