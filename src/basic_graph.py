from graph import Graph
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node
import itertools as it

def basic_square(for_lhs=False, hanging=True):
    """
    for_lhs is mostly necessary when basic_* functions are invoked from
    __create_lhs - then handles are enumerated from 0, which is very
    handy during processing of monomorphisms.
    TODO: delete `hanging' argument after P7 is introduced and change it
    to false
    """
    graph = Graph()

    edge_attrs = EdgeAttrs('q', hanging)
    if for_lhs:
        node_1 = Node(NodeAttrs(label='v', x=0, y=0, flag=False), handle=0)
        node_2 = Node(NodeAttrs(label='v', x=1, y=0, flag=False), handle=1)
        node_3 = Node(NodeAttrs(label='v', x=1, y=1, flag=False), handle=2)
        node_4 = Node(NodeAttrs(label='v', x=0, y=1, flag=False), handle=3)
        q_handle = 4
    else:
        node_1 = Node(NodeAttrs(label='v', x=0, y=0, flag=False))
        node_2 = Node(NodeAttrs(label='v', x=1, y=0, flag=False))
        node_3 = Node(NodeAttrs(label='v', x=1, y=1, flag=False))
        node_4 = Node(NodeAttrs(label='v', x=0, y=1, flag=False))
        q_handle = None

    nodes = [node_1, node_2, node_3, node_4]

    graph.add_node_collection(nodes)
    graph.add_q_hyperedge(nodes, edge_attrs, q_handle)

    # add boundry edges and set appropriate properties on them
    for node_a, node_b in it.pairwise(nodes + [node_1]):
        attr = EdgeAttrs(kind='e', flag=True)
        edge = Edge(node_a.handle, node_b.handle, attr)
        graph.add_edge(edge)

    return graph

def basic_star5(for_lhs=False, select_central=False):
    """
    warning: star is facing to the left.
    """

    graph = Graph()

    if for_lhs:
        node_1 = Node(NodeAttrs('v', 0, 0, False), 0)
        node_2 = Node(NodeAttrs('v', 1, 0, False), 1)
        node_3 = Node(NodeAttrs('v', 1, 1, False), 2)
        node_4 = Node(NodeAttrs('v', 0, 1, False), 3)
        node_5 = Node(NodeAttrs('v', 1.3, 0.5, False), 4)
        node_p = Node(NodeAttrs('p', 0.5, 0.5, select_central), 5)
    else:
        node_1 = Node(NodeAttrs('v', 0, 0, False))
        node_2 = Node(NodeAttrs('v', 1, 0, False))
        node_3 = Node(NodeAttrs('v', 1, 1, False))
        node_4 = Node(NodeAttrs('v', 0, 1, False))
        node_5 = Node(NodeAttrs('v', 1.3, 0.5, False))
        node_p = Node(NodeAttrs('p', 0.5, 0.5, select_central))

    nodes = [node_1, node_2, node_3, node_4, node_5]
    graph.add_node_collection(nodes)
    attr = EdgeAttrs('p', flag=select_central)
    graph.add_p_hyperedge(nodes, attr, node_p.handle, (0.5, 0.5)) 

    return graph, nodes

def basic_pentagon(for_lhs=False, select_central=False):

    graph, nodes = basic_star5(for_lhs=for_lhs, select_central=select_central)
    idx_nodes = [0, 1, 4, 2, 3, 0]
    nodes_shuffled = [nodes[i] for i in idx_nodes]
    for node_a, node_b in it.pairwise(nodes_shuffled):
        attr = EdgeAttrs('e', flag=True)
        edge = Edge(node_a.handle, node_b.handle, attr)
        graph.add_edge(edge)

    return graph
