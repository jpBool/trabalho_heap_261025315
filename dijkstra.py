"""Dijkstra parametrizado pela classe da fila de prioridade."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Type

Graph = Sequence[Sequence[tuple[int, float]]]


def dijkstra(graph: Graph, source: int, heap_class: Type):

    """Retorne (distancias, predecessores) usando heap_class."""

    n = len(graph)
    for node_edges in graph:
        for _, weight in node_edges:
            if weight < 0:
                raise ValueError("Pesos negativos não são permitidos")

    # Inicializa os valores de todos os nós com infinito
    distances = {node: float("inf") for node in range(n)}
    distances[source] = 0 # Define o valor de source como 0

    # Inicializa os predecessores de cada nó
    predecessors = {node: None for node in range(n)}

    # Inicializa a fila de prioridade
    pq = heap_class()
    # Lista com referências aos nós que estão em pq
    handles = {}
    handles[source] = pq.push(source, 0)

    # Cria um set para guardar os nós visitados
    visited = set()

    while True:

        try:
            # Pega o nó da heap com menor distância de source
            (current_node, current_distance) = pq.pop_min()
        except IndexError as e:
            break # Termina o laço caso a fila esteja vazia

        # Pula a iteração quando o nó já foi visitado
        if current_node in visited :
            continue
        visited.add(current_node) # Se foi visitado pela primeira vez, adiciona em visited

        # Percorre os vizinhos do nó corrente
        for neighbor, weight in graph[current_node]:
            # Não pode haver pesos negativos
            if weight < 0:
                raise ValueError("Pesos negativos não são permitidos")
            # Verifica se ja foi visitado
            if neighbor in visited:
                continue
            # Calcula a distância para com o nó o vizinho
            tentative_distance = current_distance + weight
            # Verifica se a distância já atribuída a neighbor é menor
            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                predecessors[neighbor] = current_node
                # Verifica se o nó já foi inserido na pq antes e ainda está nela
                if neighbor in handles and handles[neighbor].index != -1:
                    pq.decrease_key(handles[neighbor], tentative_distance)
                else:
                    handles[neighbor] = pq.push(neighbor, tentative_distance)

    return distances, predecessors

