from typing import Iterable
from production import Production
from graph import Graph
from model import NodeHandle, UserInput


class Driver:
    def __init__(self) -> None:
        pass


    def execute_production_sequence(self, graph: Graph, prods: Iterable[Production | UserInput]):
        for prod in prods:
            if isinstance(prod, Production):
                assert prod(graph)
            elif isinstance(prod, UserInput):
                id = prod()
                graph.update_hyperedge_flag(id, True)
            else:
                raise RuntimeError("HEHE")
