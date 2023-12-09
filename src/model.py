import itertools as it
from typing import NamedTuple, Literal, Optional, Dict
from dataclasses import dataclass, field


NodeHandle = int
EdgeHandle = int


class EdgeEndpoints(NamedTuple):
    u: NodeHandle
    v: NodeHandle


class NodeAttrs(NamedTuple):
    label: str
    x: float
    y: float
    hanging: bool

    def __str__(self, i: int = None) -> str:
        return f'{i}\nl={self.label}, h={self.hanging}\nx={self.x}, y={self.y}'


@dataclass
class EdgeAttrs:
    kind: Literal['e'] | Literal['q']
    value: bool  # Interpretation of this field depends on edge kind. See presentation with project spec.
    handle: EdgeHandle = field(default_factory=it.count().__next__, init=True)

    def __str__(self) -> str:
        return f'{self.kind}, {self.value}, {self.handle}'


@dataclass
class Node:
    attrs: NodeAttrs
    handle: NodeHandle = field(default_factory=it.count().__next__, init=True)


@dataclass
class Edge:
    u: NodeHandle
    v: NodeHandle
    attrs: EdgeAttrs

    def get_endpoints(self) -> EdgeEndpoints:
        return EdgeEndpoints(u, v)


GraphMapping = Dict[NodeHandle, NodeHandle]

