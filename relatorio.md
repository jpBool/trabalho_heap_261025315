# Relatório experimental

## Ambiente e protocolo

Os experimentos foram executados em um ambiente controlado, com as seguintes especificações de hardware e software:

<!-- Descreva máquina, Python, semente, aquecimento e repetições. -->

- **Máquina:** `Acer Nitro V15`
- **Processador:** `13th` Gen Intel(R) Core(TM) `i5-13420H`
- **S.O.:** **`Ubuntu 24.04.5 LTS`**
- **Versão do Python:** **`3.12.3`**
- **Gerador e Semente Pseudoaleatória:** os grafos foram gerados utilizando o módulo nativo `random` com a semente fixa **`SEED = 2027`**, garantindo que as três heaps sejam comparadas sobre exatamente a mesma instância de grafo em cada configuração.
- **Relógio de Medição:** `time.perf_counter()` (alta precisão).
- **Protocolo de Medição e Aquecimento (Warm-up):** para cada combinação de estrutura de dados, família de grafo e tamanho ($N$):
    * **Aquecimento:** 2 execuções descartadas (aquecimento = 2) antes da coleta, para estabilizar o interpretador e o cache do sistema operacional.
    * **Medição:** após o aquecimento, 7 medições independentes (repeticoes = 7) do algoritmo de Dijkstra isolado.
    * **Agregação:** os dados foram agregados usando a Mediana (tendência central, em segundos) e o Desvio Absoluto Mediano — MAD (dispersão, em segundos).

## Famílias de grafos

Para avaliar o custo real das operações de cada estrutura (Binary Heap, Binomial Heap e Fibonacci Heap), foram usadas três famílias de grafo:

- **Grafos Esparsos:** número de arestas próximo ao número de nós ($E \approx V$), gerado com $m \approx 4n$ arestas aleatórias.
- **Grafos Densos:** número de arestas aproximadamente igual ao quadrado do número de nós ($E \approx V^2$), grafo completo direcionado.
- **Grafos "Dijkstra Ladder":** grafo construído propositalmente para forçar o pior caso de inserções e rebaixamentos de chave (`decrease-key`) na heap, explorando a fragilidade estrutural do algoritmo.

Os tamanhos ($N$ — número de vértices) usados em cada família foram:

| | |
|-|-|
| • 100 | • 500 |
| • 1000 | • 5000 |

## Resultados

Os resultados detalhados encontram-se sumarizados nos arquivos de referência: `Heaps_Comparation.png` mostra o crescimento do tempo de execução em função do número de vértices, e `Data_Metrics.png` traz os valores exatos de Mediana e Desvio (ambos em segundos) para cada configuração.

![Comparação de Heaps](Heaps_Comparation.png)

![Métricas do Gráfico](Data_Metrics.png)

Com base nos dados coletados (valores em segundos):

1. **Grafos Esparsos:** para $N=5000$ os tempos foram minúsculos. A `BinaryHeap` teve o melhor desempenho (Mediana: ~0.027s), seguida pela `BinomialHeap` (~0.031s) e pela `FibonacciHeap` (~0.061s).
2. **Grafos Densos:** o tempo cresceu substancialmente para todas as estruturas, chegando a ~1.5s para $N=5000$. Não houve vantagem clara entre elas: `BinomialHeap` (1.533s) e `BinaryHeap` (1.535s) ficaram em empate técnico, com a `FibonacciHeap` (1.583s) muito próxima.
3. **Grafos "Dijkstra Ladder":** aqui a diferença estrutural ficou evidente em $N=5000$. A `BinomialHeap` foi a mais eficiente (~2.701s), seguida pela `FibonacciHeap` (~2.899s). A `BinaryHeap` sofreu mais com essa topologia, registrando o pior tempo do experimento (~3.343s).

Em todas as medições o Desvio (MAD) se manteve baixo, na ordem de $10^{-6}$ a $10^{-2}$ segundos, o que indica um ambiente estável e medições pouco ruidosas.

## Discussão

Os resultados refletem o peso das operações dominantes (`extract-min` e `decrease-key`) e as constantes ocultas de cada estrutura na prática, em Python.

No cenário **Esparso**, há poucas arestas, logo poucas chamadas a `decrease-key`; o custo recai sobre `extract-min`. A `BinaryHeap`, implementada sobre um array contíguo e com baixíssimo *overhead* de ponteiros, tem o melhor desempenho prático — refletindo bem seu $O(\log V)$. Já a `FibonacciHeap` paga um preço alto em alocação de objetos e manipulação de referências, o que a torna a mais lenta em grafos simples, mesmo tendo a melhor complexidade assintótica de inserção.

No cenário **Denso**, o número de arestas ($E \approx V^2$) multiplica as chamadas a `decrease-key`. Teoricamente a `FibonacciHeap` deveria vencer, já que tem custo amortizado $O(1)$ nessa operação. Na prática, porém, o peso constante de sua manipulação de listas encadeadas compensa esse ganho teórico, e as três estruturas terminam com tempos quase idênticos para $N=5000$ — um exemplo direto de como uma melhor complexidade assintótica não garante menor tempo de execução no intervalo de tamanhos testado.

O cenário **Dijkstra Ladder** é o teste que melhor separa as estruturas: como o grafo força cascatas de `decrease-key`, heaps que reorganizam a árvore de forma pouco eficiente perdem tração. A degradação da `BinaryHeap` fica clara ($O(\log V)$ por decréscimo, repetido muitas vezes). `BinomialHeap` e `FibonacciHeap` lidam melhor com essas atualizações estruturais — e o fato de a `BinomialHeap` superar a `FibonacciHeap` neste teste aponta, de novo, para o alto custo estrutural que a Fibonacci Heap carrega em Python ao fundir e atualizar suas listas encadeadas, mesmo com complexidade amortizada superior no papel.

## Limitações e ameaças à validade

1. **Constantes da linguagem interpretada:** o experimento foi feito em Python (v3.12.3). Estruturas baseadas em ponteiros (Fibonacci e Binomial) sofrem penalidades maiores por gerenciamento de objetos (Garbage Collector, ausência de localidade de cache) do que teriam em linguagens de baixo nível como C/C++.
2. **Escala de N limitada:** o maior tamanho testado foi $N=5000$. Para observar o ponto em que o custo amortizado $O(1)$ da Fibonacci Heap efetivamente supera sua constante alta em cenários densos, seria necessário escalar para $N=50000$ ou mais.
3. **Semente única:** usou-se apenas `SEED = 2027`. As 7 repetições mitigam ruído de hardware/SO, mas não o viés da topologia específica gerada por essa semente; outras sementes deveriam ser testadas para confirmar a tendência.
4. **Viés de hardware:** as execuções ocorreram em um único processador (i5-13420H), então o impacto dos níveis de cache L1/L2/L3 nas estruturas mais sensíveis a localidade de memória (como a `BinaryHeap`) reflete apenas essa arquitetura.
