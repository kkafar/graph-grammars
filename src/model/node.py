from typing import NamedTuple
from .point import Point

class NodeAttrs(NamedTuple):
    id: int
    label: str
    point: Point

    def __eq__(self, other: 'NodeAttrs'):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)