import itertools as it
from typing import NamedTuple, Literal, Optional, Dict
from dataclasses import dataclass, field

class NodeAttrs(NamedTuple):
    label: str
    x: float
    y: float
    hanging: bool

    def __str__(self, i: int = None) -> str:
        return f'{i}\nl={self.label}, h={self.hanging}\nx={self.x}, y={self.y}'

class EdgeAttrs(NamedTuple):
    kind: Literal['e'] | Literal['q']
    value: bool  # Interpretation of this field depends on edge kind. See presentation with project spec.

    def __str__(self) -> str:
        return f'kind={self.kind}, r/b={self.value}'

NodeHandle = int

@dataclass
class Node:
    attrs: NodeAttrs
    handle: NodeHandle = field(default_factory=it.count().__next__, init=True)

class Edge(NamedTuple):
    u: NodeHandle
    v: NodeHandle
    attrs: EdgeAttrs


GraphMapping = Dict[NodeHandle, NodeHandle]
