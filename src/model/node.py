from typing import NamedTuple
from .point import Point

class Node(NamedTuple):
    id: int
    label: str
    point: Point

    def __eq__(self, other: 'Node'):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)