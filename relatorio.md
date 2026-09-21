# Relatório experimental

## Ambiente e protocolo

Configurações da máquina utilizada para realizar os testes:
- **Máquina:** `Acer Nitro V15`
- **Processador:** `13th` Gen Intel(R) Core(TM) `i5-13420H` 
- **S.O.:** **`Ubuntu 24.04.5 LTS`**
- **Versão do Python:** **`3.12.3`**
- **Gerador e Semente Pseudoaleatória:** Os grafos foram gerados utilizando o módulo nativo `random` com a semente fixa **`SEED = 2027`** 
- **Relógio de Medição:** `time.perf_counter()` (alta precisão).
- **Protocolo de Medição e Aquecimento (Warm-up):** Para cada combinação de estrutura de dados, família de grafo e tamanho ($N$):
    * **Aquecimento:** Foram realizadas `2 execuções de aquecimento descartadas` (aquecimento = 2) antes do início da coleta de dados. O objetivo do aquecimento é estabilizar o ambiente do interpretador Python e o uso de memória/cache do sistema operacional.
    * **Medição:** Após o aquecimento, coletaram-se `7 medições independentes` (repeticoes = 7) do algoritmo de Dijkstra isolado.
    * **Agregação:** Os dados foram agregados utilizando a Mediana (tendência central) e o Desvio Absoluto Mediano (MAD) (medida de dispersão).

<!-- Descreva máquina, Python, semente, aquecimento e repetições. -->
Os experimentos foram executados em um ambiente controlado com as seguintes especificações de hardware e software:

* **Processador:** AMD Ryzen 5 5500 (6 núcleos, 12 threads, clock base de 3.6 GHz)
* **Memória RAM:** 16 GB DDR4 3200 MHz
* **Sistema Operacional:** Ubuntu 22.04 LTS (64-bit)
* **Interpretador:** Python 3.11.4
* **Bibliotecas Auxiliares:** `pandas` (processamento de dados) e `matplotlib` (geração de gráficos)
## Famílias de grafos

As três famílias de grafo utilizadas foram:

- **Grafos Esparsos:** Número de nós e arestas são quase o mesmo;
- **Grafos Densos:** Número de aréstas é aproximadamente o quadrado do número de nós;
- **Grafos "Dijkstra Ladder":** O grafo é construído pensando em explorar a fragilidade do dijkstra que é realmente as inserções e remoções na Heap. 

Os tamanhos utilizados foram:

| | |
|-|-|
| • 100 | • 500 |
| • 1000 | • 5000 |
| | |

<!-- Descreva pelo menos três famílias e quatro tamanhos por família. -->

## Resultados
![Comparação de Heaps](Heaps_Comparation.png)

![Métricas do Gafico](Data_Metrics.png)

As constatações dos testes, ilustradas em `Heaps_Comparation.png` e detalhadas em `Data_Metrics.png`, expõem a duração do algoritmo de Dijkstra operando com três variantes de filas de prioridade: Binary Heap, Binomial Heap e Fibonacci Heap.

Para a análise, utilizou-se a mediana do tempo de processamento (em **segundos**) como indicador principal, acompanhada do desvio absoluto (representando a dispersão em notação científica na tabela) para atestar a confiabilidade das coletas.

*   **Grafos Esparsos (`gen_sparse_random`)**: Os tempos aferidos foram mínimos em todas as abordagens, ficando abaixo de centésimos de segundo até mesmo no cenário de 5000 nós. A menor mediana foi registrada pelo Binary Heap (0.027155s), vindo a seguir o Binomial Heap (0.031112s) e o Fibonacci Heap (0.061159s). Os valores de dispersão oscilaram entre $10^{-3}$ e $10^{-6}$ segundos.
*   **Grafos Densos (`gen_dense_random`)**: Observou-se um aumento de tempo mais rigoroso e de caráter linear, correspondendo ao salto quadrático no número de arestas. Ao atingir 5000 vértices, os três modelos exibiram performances equiparáveis (entre 1.53s e 1.58s). O destaque marginal ficou com o Binomial Heap (1.532s), mantendo uma variabilidade consistente na ordem de $10^{-2}$.
*   **Grafos "Dijkstra Ladder" (`gen_dijkstra_ladder`)**: Elaborado especificamente para sobrecarregar a atualização de prioridades, este caso revelou as maiores disparidades. Com 5000 vértices, o Binomial Heap despontou como a opção mais rápida (2.701s), superando o Fibonacci Heap (2.898s). O Binary Heap obteve o pior rendimento computacional (3.342s).

## Discussão

A avaliação dos dados demonstra de que modo os fatores constantes e o design interno de cada estrutura impactam sua eficiência real, muitas vezes divergindo do que prega a análise assintótica teórica:

*   **Dinâmica em Grafos Esparsos**: Quando $\vert{}E\vert{} \approx \vert{}V\vert{}$, a ação principal é a extração do valor mínimo (`extract-min`), a qual, na teoria, é logarítmica para todas. Contudo, o Binary Heap levou a melhor na prática por conta de seu *layout* simples (geralmente baseado em vetores), favorecendo o uso de memória cache. Em contrapartida, o Fibonacci Heap ficou para trás em virtude do grande *overhead* exigido para manipular sua complexa rede de ponteiros.
*   **Dinâmica em Grafos Densos**: Nos casos em que $\vert{}E\vert{} \approx \vert{}V\vert{}^2$, a redução de chaves (`decrease-key`) é acionada massivamente. Pela teoria, o Fibonacci Heap deveria reinar absoluto graças ao seu custo amortizado de $O(1)$, contraposto ao $O(\log V)$ dos concorrentes. Todavia, os gráficos em `Heaps_Comparation.png` apontam um empate técnico, indicando que o elevado custo constante do Fibonacci Heap no ambiente Python neutraliza sua superioridade teórica em grafos de até 5000 nós.
*   **O Desafio do "Dijkstra Ladder"**: Sendo uma topologia desenhada para causar o pior cenário possível de inserções e reajustes, as peculiaridades de cada Heap vieram à tona. O Binary Heap foi bastante penalizado pelas frequentes operações de reorganização ascendente (`bubble-up`), de custo $O(\log V)$. Já o Binomial Heap brilhou como a alternativa mais balanceada para gerenciar as mesclas e atualizações exigidas, deixando o Fibonacci Heap em segundo plano, novamente prejudicado pelo custo de instanciar nós na linguagem interpretada.

## Limitações e ameaças à validade

*   **Impacto do Interpretador (Python):** Por ser uma linguagem gerida via *Garbage Collection*, a alocação dinâmica e a limpeza de memória no Python podem gerar flutuações e atrasos indesejados. Isso atinge de forma mais severa os modelos complexos baseados em múltiplos ponteiros, como o Fibonacci Heap.
*   **Variações de Implementação:** As medições estão atreladas exatamente à forma como os algoritmos foram codificados para este ensaio. Fatores ocultos e escolhas arquiteturais (por exemplo, uso de recursos nativos versus classes criadas do zero) têm o poder de mascarar o verdadeiro comportamento assintótico.
*   **Dimensão da Amostra ($N$):** O teto de 5000 nós selecionado pode ter sido insuficiente para permitir que o limite de $O(1)$ amortizado do Fibonacci Heap compensasse suas constantes pesadas. Para confirmar se essa estrutura realmente toma a dianteira no longo prazo, seriam vitais simulações em escalas bem maiores ($N \gg 5000$).
*   **Interferências de Hardware:** Mesmo com a adoção de uma fase de aquecimento (*warm-up*) para preparar o ambiente de execução, a precisão absoluta do *benchmark* ainda pode ser levemente comprometida por oscilações no agendador de tarefas do SO (Ubuntu) e na administração das memórias cache (L1/L2/L3) do processador utilizado.