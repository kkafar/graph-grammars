import networkx as nx
import graphviz
from model.graph import Graph
from model.node import NodeAttrs
from model.point import Point

def main():
    graph = Graph()
    node_1 = NodeAttrs(0, 'root', Point(0, 0))
    node_2 = NodeAttrs(1, '1', Point(1, 0))
    node_3 = NodeAttrs(2, '2', Point(1, 1))

    graph.add_node(node_1)
    graph.add_node(node_2)
    graph.add_node(node_3)

    graph.add_edge(node_1, node_2, {'foo': 'bar'})
    graph.add_edge(node_1, node_3, {'42': '84'})

    print(graph.backing_graph().nodes)
    print(graph.backing_graph().edges)
    print(list(graph.backing_graph().edges)[0])

    graph_for_vis = nx.nx_agraph.to_agraph(graph.backing_graph())
    graph_for_vis.draw("graph.png", prog='dot')


    subgraph = Graph()
    subgraph.add_edge(node_1, node_2, {'foo': 'bar'})
    # graph_for_vis = nx.nx_agraph.to_agraph(subgraph.backing_graph())
    # graph_for_vis.draw("subgraph.png", prog='dot')

    print(subgraph.backing_graph())
    list(print(graph.generate_subgraphs_isomorphic_with(subgraph)))

if __name__ == '__main__':
    main()
