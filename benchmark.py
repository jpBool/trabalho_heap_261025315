"""Experimento reproduzível; complete e gere os dados do relatório."""

from __future__ import annotations

import random
import statistics
import time
import dijkstra
import heaps

SEED = 2027

# Gera grafo esparso 
def gen_sparse_random(n : int, rng : random.Random) -> list[list]: 

    # Em grafos esparsos é esperado que m ~ n. Usaremas m = 4n como alvo 
    m_target = 4 * n # número de arestas que queremos que o grafo tenha
    graph = [[] for _ in range(n)] # grafo
    edges = set() # conjunt de vertices já conectados
    m_count = 0 # contador de arestas criadas

    while len(edges) < m_target and m_count < m_target * 20:
        u = rng.randint(0,n-1) 
        v = rng.randint(0,n-1)
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

# Gera grafo com o prior caso do dijkstra
def gen_dijkstra_ladder(n :int, rnd : random.Random):

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

def benchmark(rng : random.Random, sizes : list = [100, 500, 1000, 5000]) -> list[list]:

    # heap_types = [heaps.BinaryHeap(), heaps.BinaryHeap(), heaps.FibonacciHeap()]
    heap_types = [heaps.BinaryHeap, heaps.BinaryHeap] 
    graph = [gen_sparse_random, gen_dense_random, gen_dijkstra_ladder] 
    data = [
        {
            "name" : f"{h.__name__} {i}",
            "graph_family" : [],   
            "mediana" : [],
            "desvio" : [],
            "size" : []
        } for i,h in enumerate(heap_types)
    ]

    for size in sizes:  
        for g in graph:
            graph_temp = g(size, rng)
            for idx,h in enumerate(heap_types):

                mediana, desvio = medir(lambda : dijkstra.dijkstra(graph_temp,0,h))
                data[idx]["mediana"].append(mediana)
                data[idx]["desvio"].append(desvio)
                data[idx]["size"].append(size)
                data[idx]["graph_family"].append(f"{g.__name__}")

    return data



import matplotlib.pyplot as plt
import pandas as pd

# Suponha que 'resultados' seja a variável que recebeu o retorno da sua função benchmark()
# resultados = benchmark(rng, sizes=[100, 500, 1000, 5000])

def visualizar_benchmark(data):
    # 1. Achatar os dados para um formato tabular (ideal para o Pandas)
    linhas = []
    for heap in data:
        for i in range(len(heap["size"])):
            linhas.append({
                "Heap": heap["name"],
                "Size": heap["size"][i],
                "Graph": heap["graph_family"][i],
                "Mediana": heap["mediana"][i],
                "Desvio": heap["desvio"][i]
            })
            
    df = pd.DataFrame(linhas)
    
    # 2. Descobrir quais são as famílias de grafos únicas para criar os subplots
    familias_grafos = df["Graph"].unique()
    
    # Cria uma figura com N gráficos lado a lado (1 linha, N colunas)
    fig, axes = plt.subplots(1, len(familias_grafos), figsize=(16, 5), sharey=True)
    
    # Se houver apenas 1 tipo de grafo, o axes não é uma lista, então forçamos ser uma
    if len(familias_grafos) == 1:
        axes = [axes]
        
    # 3. Plotar os dados
    for i, nome_grafo in enumerate(familias_grafos):
        ax = axes[i]
        
        # Filtra os dados apenas para o grafo atual
        df_grafo = df[df["Graph"] == nome_grafo]
        
        # Plota uma linha para cada tipo de Heap
        for nome_heap in df_grafo["Heap"].unique():
            df_heap = df_grafo[df_grafo["Heap"] == nome_heap]
            
            # Ordena pelo tamanho para a linha não ficar embaralhada
            df_heap = df_heap.sort_values(by="Size")
            
            # Desenha a linha principal (Mediana)
            ax.plot(df_heap["Size"], df_heap["Mediana"], marker='o', label=nome_heap)
            
            # Desenha a margem de erro (Desvio Padrão) como uma sombra
            ax.fill_between(
                df_heap["Size"], 
                df_heap["Mediana"] - df_heap["Desvio"], 
                df_heap["Mediana"] + df_heap["Desvio"], 
                alpha=0.2 # Transparência
            )
            
        ax.set_title(f"Grafo: {nome_grafo}")
        ax.set_xlabel("Número de Vértices (Size)")
        ax.set_ylabel("Tempo de Execução (Nanosegundos)")
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()

    plt.tight_layout()
    plt.show()

# Chamando a função:
# visualizar_benchmark(resultados)
def main() -> None:
    random.seed(SEED)
    rnd = random.Random()

    data = benchmark(rnd, [10])
    visualizar_benchmark(data)

    return 1
    raise NotImplementedError("Implemente o protocolo descrito no enunciado")


if __name__ == "__main__":
    main()

