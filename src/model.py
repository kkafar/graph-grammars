import itertools as it
from typing import NamedTuple, Literal, Optional, Dict, Callable
from dataclasses import dataclass, field


NodeHandle = int
EdgeHandle = int


class EdgeEndpoints(NamedTuple):
    u: NodeHandle
    v: NodeHandle


@dataclass
class NodeAttrs:
    label: Literal['v'] | Literal['q'] | Literal['p']
    x: float
    y: float
    flag: Optional[bool]  # Interpretation of this field depends on edge kind. See presentation with project spec

    def __str__(self, i: int = None) -> str:
        # return (f'{i}, ' if i is not None else '') + f'{self.label}, {self.flag}'
        return (f'{self.label},{i},{self.flag}')


@dataclass
class EdgeAttrs:
    kind: Literal['e'] | Literal['q'] | Literal['p']
    flag: bool  # Interpretation of this field depends on edge kind. See presentation with project spec.
    handle: EdgeHandle = field(default_factory=it.count().__next__, init=True)

    def __str__(self) -> str:
        return f'{self.flag}'


class Node:
    __slots__ = (
        'attrs',
        'handle'
    )

    def __init__(self, attrs: NodeAttrs, handle: NodeHandle = None, handle_factory: Callable[[], int] = None) -> None:
        self.attrs: NodeAttrs = attrs
        self.handle: NodeHandle = handle

        if self.handle is None and handle_factory is not None:
            self.handle = handle_factory()
            assert self.handle is not None

    def __str__(self) -> str:
        return f'Node(attrs=NodeAttrs(l={self.attrs.label}, x={self.attrs.x}, y={self.attrs.y}, flag={self.attrs.flag}), handle={self.handle})'


@dataclass
class Edge:
    u: NodeHandle
    v: NodeHandle
    attrs: EdgeAttrs

    def get_endpoints(self) -> EdgeEndpoints:
        return EdgeEndpoints(self.u, self.v)


GraphMapping = Dict[NodeHandle, NodeHandle]

