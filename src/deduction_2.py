from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node, GraphMapping
from graph import Graph
from matplotlib import pyplot as plt
from production import P1, P2, P3, P7, P8, P11, P17

def base_graph():
    G = Graph()
    
    node_0 = Node(NodeAttrs('v', 0, 0, False))
    node_1 = Node(NodeAttrs('v', 3, 0, False))
    node_2 = Node(NodeAttrs('v', 4, -1.5, False))
    node_3 = Node(NodeAttrs('v', 3, -3, False))
    node_4 = Node(NodeAttrs('v', 0, -3, False))
    node_5 = Node(NodeAttrs('v', -2, 2, False))
    node_6 = Node(NodeAttrs('v', 5, 2, False))

    node_7 = Node(NodeAttrs('v', 5, -1.5, False)) # outer

    node_8 = Node(NodeAttrs('v', 5, -5, False))
    node_9 = Node(NodeAttrs('v', -2, -5, False))

    nodes = [node_0, node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9]
    G.add_node_collection(nodes)
    
    edges = [
        Edge(node_0.handle, node_1.handle, EdgeAttrs('e', False)),
        Edge(node_1.handle, node_2.handle, EdgeAttrs('e', False)),
        Edge(node_2.handle, node_3.handle, EdgeAttrs('e', False)),
        Edge(node_3.handle, node_4.handle, EdgeAttrs('e', False)),
        Edge(node_4.handle, node_0.handle, EdgeAttrs('e', False)),
        Edge(node_0.handle, node_5.handle, EdgeAttrs('e', False)),
        Edge(node_1.handle, node_6.handle, EdgeAttrs('e', False)),
        Edge(node_2.handle, node_7.handle, EdgeAttrs('e', False)),
        Edge(node_3.handle, node_8.handle, EdgeAttrs('e', False)),
        Edge(node_4.handle, node_9.handle, EdgeAttrs('e', False)),
        Edge(node_5.handle, node_6.handle, EdgeAttrs('e', True)),
        Edge(node_6.handle, node_7.handle, EdgeAttrs('e', True)),
        Edge(node_7.handle, node_8.handle, EdgeAttrs('e', True)),
        Edge(node_8.handle, node_9.handle, EdgeAttrs('e', True)),
        Edge(node_9.handle, node_5.handle, EdgeAttrs('e', True))
    ]

    G.add_edge_collection(edges)

    G.add_q_hyperedge((node_0, node_1, node_6, node_5), EdgeAttrs('q', False))
    G.add_q_hyperedge((node_1, node_2, node_7, node_6), EdgeAttrs('q', False))
    G.add_q_hyperedge((node_2, node_3, node_8, node_7), EdgeAttrs('q', False))
    G.add_q_hyperedge((node_3, node_4, node_9, node_8), EdgeAttrs('q', False))
    G.add_q_hyperedge((node_0, node_4, node_9, node_5), EdgeAttrs('q', False))
    G.add_p_hyperedge((node_0, node_1, node_2, node_3, node_4), EdgeAttrs('p', False))

    G.display()
    plt.show()

    
    P1()(G)
    P2()(G)
    P11()(G)
    P1()(G)
    P2()(G)
    P3()(G)
    P1()(G)

    G.display()
    plt.show()

if __name__ == "__main__":
    base_graph()