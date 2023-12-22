import networkx as nx
import graphviz
import itertools as it
import matplotlib.pyplot as plt
import argparse
import importlib
from typing import Optional
from dataclasses import dataclass, field
from model import NodeHandle, NodeAttrs, EdgeAttrs, Node, Edge
from graph import Graph
from production import Production, P1, P2, P5, P6

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


if __name__ == '__main__':
    main()

