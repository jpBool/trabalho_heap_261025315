# Relatório experimental

## Ambiente e protocolo

Congfigurações da máquina utilizada para realizar os testes:
- Máquina: Acer Nitro V15
- Processador: 13th Gen Intel(R) Core(TM) i5-13420H 
- S.O.: **`Ubuntu 24.04.5 LTS`**
- Versão do Python: ** 3.12.3 **
- Gerador e Semente Pseudoaleatória:** Os grafos foram gerados utilizando o módulo nativo `random` com a semente fixa **`SEED = 2027`** 
- Protocolo:
    Para cada combinação de **estrutura de dados** (Heap Binária vs. Heap de Fibonacci), **família de grafo** (`gen_sparse_random`, `gen_dense_random` e `gen_dijkstra_ladder`) e **tamanho de entrada**:

    1. **Isolamento do Algoritmo:** A geração da estrutura do grafo ocorre antes da medição. Cronometra-se estritamente a execução do algoritmo de Dijkstra (`dijkstra.dijkstra(graph_temp, 0, h)`), ignorando o tempo de alocação de memória do grafo.
    2. **Amostragem e Repetições:** Cada teste é repetido de forma independente por **7 vezes** (`repeticoes = 7`) sobre a mesma instância para mitigar ruídos e oscilações do sistema operacional.
    3. **Estatística Robusta (Tendência Central e Dispersão):**
        * **Medida de Tendência Central:** Utilizou-se a **Mediana** dos tempos de execução. A mediana é preferível à média por ser uma estatística robusta, imune a *outliers* causados por picos pontuais de uso de CPU ou *Garbage Collection*.
        * **Medida de Dispersão:** Utilizou-se o **Desvio Absoluto Mediano** (**MAD** — *Median Absolute Deviation*), calculado como `median(|t_i - mediana|)`, representando a variabilidade real das medições.

<!-- Descreva máquina, Python, semente, aquecimento e repetições. -->

## Famílias de grafos

As três famílias de grafo utilizadas foram:

- Grafos Esparsos : Número de nós e arestas são quase o mesmo;
- Grafos Densos : Número de aréstas é aproximadamente o quadrado do número de nós;
- Grafos "Dijkstra Ladder" : O grafo é construído pensando em explorar a fragilidade do dijkstra que é realmente as inserções e remoções na Heap. 

Os tamanhos utilizados foram:

| | |
|-|-|
| • 100 | • 500 |
| • 1000 | • 5000 |
| | |

<!-- Descreva pelo menos três famílias e quatro tamanhos por família. -->

## Resultados
<!-- Inclua unidades e dispersão. -->

## Discussão

<!-- Relacione resultados, operações dominantes e análise assintótica. -->

## Limitações e ameaças à validade

