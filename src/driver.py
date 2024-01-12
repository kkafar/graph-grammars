from typing import Iterable
from production import Production
from graph import Graph
from model import NodeHandle


class InputProvider:
    """ This class is used by the `Driver` to get handle of hyperedge marked for breaking.
    """
    def __call__(self):
        raise NotImplementedError("__call__ must be implemented")


class FixedInput(InputProvider):
    """ Use this class to provide driver with fixed node handle to mark for breaking.
    """
    def __init__(self, hypernode_handle: NodeHandle) -> None:
        assert hypernode_handle is not None
        self.handle = hypernode_handle

    def __call__(self):
        return self.handle


class UserInput(InputProvider):
    """ Use this class to let user decide what node should be marked for breaking.
    """
    def __call__(self) -> NodeHandle:
        return int(input("NodeHandle>"))


class Driver:
    def execute_production_sequence(self, graph: Graph, prods: Iterable[Production | InputProvider]):
        for prod in prods:
            if isinstance(prod, Production):
                assert prod(graph)
            elif isinstance(prod, InputProvider):
                graph.update_hyperedge_flag(prod(), True)
            else:
                raise RuntimeError("HEHE")
