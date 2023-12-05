import networkx as nx
import graphviz
import itertools as it
import matplotlib.pyplot as plt
from model.graph import Graph, Node, NodeAttrs, EdgeAttrs, EdgeType

def main():
    graph = Graph()

    node_attrs = (
        NodeAttrs('first', 0, 0),
        NodeAttrs('second', 1, 1),
        NodeAttrs('third', 2, 4)
    )

    bundles = list(zip(range(len(node_attrs)), node_attrs))
    graph.add_node_collection(bundles)

    for (node_1, _), (node_2, _) in it.pairwise(bundles):
        graph.add_edge(node_1, node_2, attrs={'foo': 'bar'})

    print(graph.nx_graph.nodes)
    print(graph.nx_graph.edges)

    subgraph = Graph()
    subgraph.add_node_collection(bundles[:2])
    for (node_1, _), (node_2, _) in it.pairwise(bundles[:2]):
        subgraph.add_edge(node_1, node_2, attrs=None)

    gm = nx.isomorphism.GraphMatcher(graph.nx_graph, subgraph.nx_graph)

    print('Mapping')
    for mapping in gm.subgraph_isomorphisms_iter():
        print(mapping)

    fig, plots = plt.subplots(nrows=1, ncols=2)
    graph.display(ax=plots[0])
    subgraph.display(ax=plots[1])

    fig.savefig('graphs.png')
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    plt.rcParams['figure.figsize'] = (16, 9)
    main()
