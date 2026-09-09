"""Experimento reproduzível; complete e gere os dados do relatório."""

from __future__ import annotations

import random
import statistics
import time

SEED = 2027

# Gera grafo esparso 
def gen_sparse_random(n : int, rng : random.Random) -> list[list]: 

    # Em grafos esparsos é esperado que m ~ n. Usaremas m = 4n como alvo 
    m_target = 4 * n # número de arestas que queremos que o grafo tenha
    graph = [[] for _ in range(n)] # grafo
    edges = set() # conjunt de vertices já conectados
    m_count = 0 # contador de arestas criadas

    while len(edges) < m_target and m_count < m_target * 20:
        u = rng.randrange(n) 
        v = rng.randrange(n)
        m_count += 1
        if u == v or (u, v) in edges:
            continue
        edges.add((u, v))
        graph[u].append((v, rng.uniform(1, 100)))

    return graph

# Gera grafo denso
def gen_dense_random(n: int, rng : random.Random) -> list[list]:

    # Em grafos esparsos é esperado que m ~ n^2.
    graph = [[] for _ in range(n)]  

    # Conectamos todos os nós entre todos os nós
    for i in range(n):
        for j in range(n):

            if(i == j):
                continue
            
            graph[i].append((j, rng.uniform(1,100)))

    return graph

def gen_dijkstra_ladder(n :int):

    base_weight = n * 2

    grafo = [[] for _ in range(n)]
    
    for i in range(n-1):
        grafo[i].append((i+1, base_weight))
    
    for i in range(n - 2):
        for j in range(i + 2, n):
            w = (j - i) * base_weight - 1
            grafo[i].append((j, w))
            
    return grafo





def medir(func, repeticoes: int = 7) -> tuple[float, float]:
    """Retorne mediana e desvio absoluto mediano, em segundos."""
    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        func()
        tempos.append(time.perf_counter() - inicio)
    mediana = statistics.median(tempos)
    mad = statistics.median(abs(t - mediana) for t in tempos)
    return mediana, mad


def main() -> None:
    random.seed(SEED)
    raise NotImplementedError("Implemente o protocolo descrito no enunciado")


if __name__ == "__main__":
    main()

