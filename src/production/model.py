import itertools as it
from copy import deepcopy
import matplotlib.pyplot as plt
import util
from typing import Dict, Optional
from model import NodeAttrs, EdgeAttrs, NodeHandle, Edge, Node, GraphMapping
from graph import Graph
from pprint import pprint
from util import verify_central_hyperedges
from itertools import combinations

class Production:
    """ Base class for all productions """
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        """ Reset state of the production so that it can be applied again. """
        self._rev_mapping = None

    def get_lhs(self) -> Graph:
        raise NotImplementedError("This method must be overrided in subclasses")

    def is_mapping_feasible(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> bool:
        """ Checks whether the production can be applied on given mapping.

        :param graph: the original 'state' graph
        :param mapping: mapping between subgraph of graph & production lhs,
        see https://networkx.org/documentation/stable/reference/algorithms/isomorphism.vf2.html#subgraph-isomorphism
        for details.

        :return: bool is the production can be successfully applied, false if not"""
        return True
        # raise NotImplementedError("This method must be overrided in subclasses")

    def apply(self, graph: Graph) -> bool:
        self.reset()
        lhs = self.get_lhs()

        if self.requires_monomorphism():
            mapping_gen = graph.generate_subgraphs_monomorphic_with(lhs)
        else:
            mapping_gen = graph.generate_subgraphs_isomorphic_with(lhs)

        for mapping in mapping_gen:
            self._rev_mapping = util.reverse_dict_mapping(mapping)
            if self.is_mapping_feasible(graph, mapping):
                self.apply_with_mapping(graph, mapping)
                return True
        return False

    def apply_with_mapping(self, graph: Graph, mapping: Dict[NodeHandle, NodeHandle]) -> None:
        """ Implement the production by overriding this method.
        This method should mutate the graph passed as argument.

        :param graph: the original 'state' graph
        :param mapping: mapping between subgraph of graph & production lhs,
        see https://networkx.org/documentation/stable/reference/algorithms/isomorphism.vf2.html#subgraph-isomorphism
        for details.

        Please note that this method is called only if `is_mapping_feasible` returned True for `mapping`."""
        raise NotImplementedError("This method must be overrided in subclasses")

    def __call__(self, graph: Graph) -> bool:
        return self.apply(graph)


    def requires_monomorphism(self) -> bool:
        """ Return True from this method if your production requires monomorphism instead of subgraph isomorphism.

        Q: How do I know whether my production requires monomorphism?
        A: Implement it first & see whether you receive appropriate mappings. If not, override this method and return False.
        You will need it most likely in productions that operate only on some subset of the whole set of edges of the node-induced subgraph.
        Read this section for more info: https://networkx.org/documentation/stable/reference/algorithms/isomorphism.vf2.html#subgraph-isomorphism
        """
        return False

