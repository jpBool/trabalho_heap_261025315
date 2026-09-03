"""Dijkstra parametrizado pela classe da fila de prioridade."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Type

Graph = Sequence[Sequence[tuple[int, float]]]


def dijkstra(graph: Graph, source: int, heap_class: Type):
    """Retorne (distancias, predecessores) usando heap_class."""
    raise NotImplementedError

