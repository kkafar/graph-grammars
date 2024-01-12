import matplotlib.pyplot as plt
import argparse
import importlib
from typing import Optional
from dataclasses import dataclass
from production import P1
from production import P2
from production import P7
from production import P8
from graph import Graph
from model import Node, NodeAttrs, Edge, EdgeAttrs
import itertools as it
import util

@dataclass
class Args:
    example_name: Optional[str] = None


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', required=False, type=str,
                        dest='example_name', help='Name of the example to run; if not specified all examples will be run one by one')
    return parser


def configure_env():
    plt.rcParams['figure.figsize'] = (16, 9)


def run_example(example_name: str):
    if example_name is None:
        example_name = 'example'
    else:
        example_name = 'example.' + example_name

    try:
        module = importlib.import_module(example_name)
        module.main()
    except ImportError:
        print(f"Failed to import module with name {example_name}")
        return


def main():
    configure_env()
    args: Args = build_cli().parse_args()
    run_example(args.example_name)


def find_mapping_to_mark_for_p7(graph):
    mappings = graph.generate_subgraphs_monomorphic_with(P7().get_lhs())

    for mapping in mappings:

        upper_right_found = False
        right_found = False
        for node_id in mapping.values():
            node = graph.node_for_handle(node_id)
            if node.attrs.x == 1 and node.attrs.y == 1:
                upper_right_found = True
            elif node.attrs.x == 1:
                right_found = True
        if upper_right_found and right_found:
            return mapping

def execute_prod_with_plot(graph, prod, find):
    graph.display(ax=plots[0])
    plots[0].set(title='Before')

    if find:
        mapping = find_mapping_to_mark_for_p7(graph)
        p7._rev_mapping = util.reverse_dict_mapping(mapping)
        assert p7.apply_with_mapping(graph, mapping)
    else:
        assert prod(graph)

    graph.display(ax=plots[1])
    plots[1].set(title='After')

    fig.suptitle(f"Applying production {prod.__class__.__name__}")
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    # main()

    fig, plots = plt.subplots(nrows=1, ncols=2)

    p1 = P1()
    p2 = P2()
    p7 = P7()
    p8 = P8()

    # TODO: create first graph
    graph = Graph()

    inner_nodes = [
        Node(NodeAttrs('v', 0, 0, False)),
        Node(NodeAttrs('v', 1, 0, False)),
        Node(NodeAttrs('v', 1.5, 0.5, False)),
        Node(NodeAttrs('v', 1, 1, False)),
        Node(NodeAttrs('v', 0, 1, False)),
    ]

    outer_nodes = [
        Node(NodeAttrs('v', -1, -1, False)),
        Node(NodeAttrs('v', 2, -1, False)),
        Node(NodeAttrs('v', 2, 0.5, False)),
        Node(NodeAttrs('v', 2, 2, False)),
        Node(NodeAttrs('v', -1, 2, False)),
    ]

    graph.add_node_collection(inner_nodes)
    graph.add_node_collection(outer_nodes)

    for node_u, node_v in it.pairwise(inner_nodes + [inner_nodes[0]]):
        graph.add_edge(Edge(node_u.handle, node_v.handle, EdgeAttrs('e', False)))

    for node_u, node_v in it.pairwise(outer_nodes + [outer_nodes[0]]):
        graph.add_edge(Edge(node_u.handle, node_v.handle, EdgeAttrs('e', True)))

    graph.add_p_hyperedge(inner_nodes, EdgeAttrs('p', False))

    for node_u, node_v in zip(inner_nodes, outer_nodes):
        graph.add_edge(Edge(node_u.handle, node_v.handle, EdgeAttrs('e', False)))


    for (node_a, node_b), (node_c, node_d) in zip(it.pairwise(inner_nodes + [inner_nodes[0]]), it.pairwise(outer_nodes + [outer_nodes[0]])):
        graph.add_q_hyperedge((node_a, node_b, node_c, node_d), EdgeAttrs('q', False))
    
    # Wywod
    execute_prod_with_plot(graph, p7, True)
    execute_prod_with_plot(graph, p1, False)
    execute_prod_with_plot(graph, p7, True)
    execute_prod_with_plot(graph, p8, False)
    execute_prod_with_plot(graph, p2, False)
    execute_prod_with_plot(graph, p1, False)
    execute_prod_with_plot(graph, p7, True)
    execute_prod_with_plot(graph, p8, False)
    execute_prod_with_plot(graph, p2, False)
    execute_prod_with_plot(graph, p1, False)
