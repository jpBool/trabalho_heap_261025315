"""Implemente as três filas de prioridade sem usar heapq."""

from __future__ import annotations
import math

class BinaryHeap:
    class _Handle:
        __slots__ = ('vertex', 'priority', 'index')

        def __init__(self, vertex: int, priority: float, index: int):
            # guarda os dados do nó e a posição dele na lista
            self.vertex = vertex
            self.priority = priority
            self.index = index
        
    def __init__(self):
        # a lista principal que funciona como a árvore do heap
        self._data: list[BinaryHeap._Handle] = []

    def push(self, vertex: int, priority: float):
        # cria o nó e adiciona no final da lista
        handle = self._Handle(vertex, priority, len(self._data))
        self._data.append(handle)
        # faz o nó subir pra posição certa pra manter a ordem
        self._sift_up(len(self._data) - 1)
        return handle

    def decrease_key(self, handle, new_priority: float) -> None:
        # checa se não tá tentando aumentar o valor (o que daria erro)
        if new_priority > handle.priority:
            raise ValueError("A nova prioridade não pode ser maior que a prioridade atual")
        handle.priority = new_priority
        # como o valor diminuiu, o nó precisa subir na árvore
        self._sift_up(handle.index)

    def pop_min(self) -> tuple[int, float]:
        if not self._data:
            raise IndexError("A fila de prioridade tá vazia")
        
        # o menor valor do heap sempre fica na raiz (índice 0)
        min_handle = self._data[0]
        # tira o último elemento da lista
        last_handle = self._data.pop()
        
        if self._data:
            # coloca o último elemento na raiz
            self._data[0] = last_handle
            last_handle.index = 0
            # empurra ele pra baixo até achar a posição certa dele
            self._sift_down(0)
            
        min_handle.index = -1
        return (min_handle.vertex, min_handle.priority)

    def __len__(self) -> int:
        return len(self._data)

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            # acha o índice do pai do nó atual
            parent = (idx - 1) // 2
            # se o nó atual for menor que o pai, eles trocam de lugar
            if self._data[idx].priority < self._data[parent].priority:
                self._swap(idx, parent)
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._data)
        while True:
            smallest = idx
            # acha os índices dos filhos da esquerda e da direita
            left = 2 * idx + 1
            right = 2 * idx + 2

            # vê quem é o menor de todos: o pai, o filho esquerdo ou o direito
            if left < n and self._data[left].priority < self._data[smallest].priority:
                smallest = left
            if right < n and self._data[right].priority < self._data[smallest].priority:
                smallest = right

            # se o pai não for o menor, troca ele com o filho menor e continua descendo
            if smallest != idx:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        # troca dois nós de lugar na lista e atualiza o índice salvo dentro deles
        self._data[i], self._data[j] = self._data[j], self._data[i]
        self._data[i].index = i
        self._data[j].index = j


class BinomialHeap:
    class Handle:
        __slots__ = ('vertex', 'priority', 'node', 'index')

        def __init__(self, vertex: int, priority: float):
            self.vertex = vertex
            self.priority = priority
            self.node: BinomialHeap.Node | None = None
            self.index = 0

    class Node:
        __slots__ = ('handle', 'degree', 'parent', 'child', 'sibling')

        def __init__(self, handle: BinomialHeap.Handle):
            self.handle = handle
            handle.node = self
            self.degree = 0
            self.parent: BinomialHeap.Node | None = None
            self.child: BinomialHeap.Node | None = None
            self.sibling: BinomialHeap.Node | None = None

    def __init__(self):
        # guarda o ponteiro pra primeira raiz da lista de árvores
        self.head: BinomialHeap.Node | None = None
        self.total_nodes = 0

    def push(self, vertex: int, priority: float) -> BinomialHeap.Handle:
        # cria o handle (que vai pro dijkstra) e o nó (que vai pra árvore)
        handle = self.Handle(vertex, priority)
        node = self.Node(handle)
        
        self.head = self._union(self.head, node)
        self.total_nodes += 1
        return handle

    def decrease_key(self, handle: BinomialHeap.Handle, new_priority: float) -> None:
        if new_priority > handle.priority:
            raise ValueError("A nova prioridade não pode ser maior que a prioridade atual")

        handle.priority = new_priority
        curr = handle.node
        parent = curr.parent

        # se o nó ficou menor que o pai, trocamos os handles entre eles
        while parent is not None and curr.handle.priority < parent.handle.priority:
            # Troca os handles associados aos nós
            curr.handle, parent.handle = parent.handle, curr.handle
            
            # Atualiza os ponteiros dos handles para apontarem para os novos nós corretos
            curr.handle.node = curr
            parent.handle.node = parent
            
            # Sobe um nível para continuar verificando
            curr = parent
            parent = curr.parent

    def pop_min(self) -> tuple[int, float]:
        if self.head is None:
            raise IndexError("A fila de prioridade tá vazia")

        # procura a raiz que tem a menor prioridade
        min_node = self.head
        min_prev = None

        curr = self.head
        prev = None

        while curr.sibling is not None:
            if curr.sibling.handle.priority < min_node.handle.priority:
                min_node = curr.sibling
                min_prev = curr
            curr = curr.sibling

        # tira a menor raiz da lista principal
        if min_prev is None:
            self.head = min_node.sibling
        else:
            min_prev.sibling = min_node.sibling

        # inverte a lista de filhos do nó removido
        children_head = None
        curr_child = min_node.child
        while curr_child is not None:
            next_child = curr_child.sibling
            curr_child.sibling = children_head
            curr_child.parent = None
            children_head = curr_child
            curr_child = next_child

        # junta as raízes que sobraram com a nova lista de filhos
        self.head = self._union(self.head, children_head)
        self.total_nodes -= 1
        
        # invalida o handle removido para o Dijkstra
        min_handle = min_node.handle
        min_handle.index = -1
        min_handle.node = None

        return (min_handle.vertex, min_handle.priority)

    def __len__(self) -> int:
        return self.total_nodes

    def _link(self, y: BinomialHeap.Node, x: BinomialHeap.Node) -> None:
        y.parent = x
        y.sibling = x.child
        x.child = y
        x.degree += 1

    def _merge_roots(
        self, h1: BinomialHeap.Node | None, h2: BinomialHeap.Node | None
    ) -> BinomialHeap.Node | None:
        if not h1:
            return h2
        if not h2:
            return h1

        if h1.degree <= h2.degree:
            head = h1
            h1 = h1.sibling
        else:
            head = h2
            h2 = h2.sibling

        tail = head
        while h1 is not None and h2 is not None:
            if h1.degree <= h2.degree:
                tail.sibling = h1
                h1 = h1.sibling
            else:
                tail.sibling = h2
                h2 = h2.sibling
            tail = tail.sibling

        tail.sibling = h1 if h1 is not None else h2
        return head

    def _union(
        self, h1: BinomialHeap.Node | None, h2: BinomialHeap.Node | None
    ) -> BinomialHeap.Node | None:
        head = self._merge_roots(h1, h2)
        if head is None:
            return None

        prev: BinomialHeap.Node | None = None
        curr: BinomialHeap.Node | None = head
        next_node: BinomialHeap.Node | None = curr.sibling

        while next_node is not None:
            if curr.degree != next_node.degree or (
                next_node.sibling is not None and next_node.sibling.degree == curr.degree
            ):
                prev = curr
                curr = next_node
            elif curr.handle.priority <= next_node.handle.priority:
                curr.sibling = next_node.sibling
                self._link(next_node, curr)
            else:
                if prev is None:
                    head = next_node
                else:
                    prev.sibling = next_node
                self._link(curr, next_node)
                curr = next_node

            next_node = curr.sibling

        return head


# Adaptação do código que está no github:
# https://github.com/danielborowski/fibonacci-heap-python/blob/master/fib-heap.py
class FibonacciHeap:
    """Estrutura de dados Fibonacci Heap (FAP), otimizada para operações

    como diminuição de chave (O(1) amortizado) e remoção do mínimo (O(log n)
    amortizado).
    """

    class Node:
        """Representa um nó individual na Fibonacci Heap."""

        def __init__(self, vertex, priority):
            self.vertex = vertex  # Identificador/valor do vértice/elemento
            self.priority = priority  # Chave de ordenação (prioridade)

            # Ponteiros para a estrutura de lista duplamente ligada circular
            self.parent = (
                self.child
            ) = self.left = self.right = None  # Ponteiros do nó

            self.degree = 0  # Número de filhos diretos do nó
            self.mark = False  # Indica se o nó perdeu um filho desde que se tornou filho de parent
            self.index = 0  # Índice auxiliar/rastreador do nó

    def __init__(self):
        """Inicializa uma Fibonacci Heap vazia."""
        self.root_list = None  # Ponteiro para a lista circular de raízes
        self.min_node = (
            None  # Ponteiro para o nó de menor prioridade (mínimo global)
        )
        self.total_nodes = 0  # Quantidade total de nós armazenados

    def __len__(self) -> int:
        """Retorna a quantidade de nós presentes na Heap."""
        return self.total_nodes

    def _iterate(self, head):
        """Gerador interno para percorrer com segurança uma lista circular duplamente ligada

        começando a partir do nó 'head'.
        """
        node = stop = head
        flag = False
        while True:
            # Para ao retornar ao ponto de partida na segunda passagem
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    def push(self, vertex: int, priority: float):
        """Insere um novo elemento na Heap.

        Complexidade: O(1).
        """
        n = self.Node(vertex, priority)
        # O nó começa isolado apontando para si mesmo (lista circular)
        n.left = n.right = n

        # Insere o novo nó na lista principal de raízes
        self._merge_with_root_list(n)

        # Atualiza o nó mínimo, se necessário
        if self.min_node is None or n.priority < self.min_node.priority:
            self.min_node = n

        self.total_nodes += 1
        return n  # Retorna o nó para permitir o uso posterior em decrease_key

    def decrease_key(self, handle, new_priority: float) -> None:
        """Reduz a prioridade de um nó existente.

        Complexidade: O(1) amortizado.
        """
        x = handle
        if new_priority > x.priority:
            raise ValueError("new_priority deve ser <= à prioridade atual")

        x.priority = new_priority
        y = x.parent

        # Se a propriedade da heap foi violada (filho com menor prioridade que o pai)
        if y is not None and x.priority < y.priority:
            self._cut(x, y)  # Corta a ligação de x com seu pai y
            self._cascading_cut(y)  # Realiza cortes em cadeia se necessário

        # Atualiza o nó mínimo global, se necessário
        if x.priority < self.min_node.priority:
            self.min_node = x

    def pop_min(self) -> tuple[int, float]:
        """Remove e retorna o nó de menor prioridade (vértice, prioridade).

        Complexidade: O(log n) amortizado.
        """
        z = self.min_node
        if z is None:
            raise IndexError("pop_min chamado em heap vazia")

        # Se o nó mínimo possui filhos, move todos os seus filhos para a lista de raízes
        if z.child is not None:
            children = [x for x in self._iterate(z.child)]
            for c in children:
                self._merge_with_root_list(c)
                c.parent = None

        # Remove z da lista principal de raízes
        self._remove_from_root_list(z)

        # Se z era o único nó da heap
        if z == z.right:
            self.min_node = self.root_list = None
        else:
            # Define temporariamente o mínimo e reorganiza a heap
            self.min_node = z.right
            self._consolidate()

        self.total_nodes -= 1
        z.index = -1  # Marca o nó como removido
        return (z.vertex, z.priority)

    def _cut(self, x, y):
        """Remove x da lista de filhos de y e o move para a lista de raízes."""
        self._remove_from_child_list(y, x)
        y.degree -= 1
        self._merge_with_root_list(x)
        x.parent = None
        x.mark = False  # Reseta a marcação pois x agora é uma raiz

    def _cascading_cut(self, y):
        """Propaga o corte para cima na árvore se o pai y já havia perdido um filho anteriormente."""
        z = y.parent
        if z is not None:
            if y.mark is False:
                # Marca y como 'tendo perdido um filho'
                y.mark = True
            else:
                # Se y já estava marcado, corta y do seu pai z e propaga recursivamente
                self._cut(y, z)
                self._cascading_cut(z)

    def _consolidate(self):
        """Reduz a quantidade de árvores na lista de raízes garantindo que

        nenhuma árvore no nível superior tenha o mesmo grau (degree).
        """
        size = max(self.total_nodes, 2)
        # Array auxiliar onde o índice representa o grau da árvore
        A = [None] * (int(math.log(size, 2)) + 2)

        nodes = [w for w in self._iterate(self.root_list)]
        for x in nodes:
            d = x.degree
            # Funde árvores do mesmo grau até que todos os graus fiquem únicos
            while d < len(A) and A[d] is not None:
                y = A[d]
                if x.priority > y.priority:
                    x, y = y, x  # Garante que x seja sempre a menor raiz
                self._heap_link(y, x)  # Torna y filho de x
                A[d] = None
                d += 1

            # Garante que o array A seja expandido se d ultrapassar o tamanho atual
            if d >= len(A):
                A.append(None)
            A[d] = x

        # Recalcula o nó mínimo global iterando sobre os nós restantes
        for node in A:
            if node is not None and node.priority < self.min_node.priority:
                self.min_node = node

    def _heap_link(self, y, x):
        """Liga duas árvores do mesmo grau, tornando y um filho de x."""
        self._remove_from_root_list(y)
        y.left = y.right = y
        self._merge_with_child_list(x, y)
        x.degree += 1
        y.parent = x
        y.mark = False

    def _merge_with_root_list(self, node):
        """Insere um nó na lista circular principal de raízes."""
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    def _merge_with_child_list(self, parent, node):
        """Insere um nó na lista circular de filhos do nó pai (parent)."""
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    def _remove_from_root_list(self, node):
        """Remove um nó da lista principal de raízes ajustando os ponteiros dos vizinhos."""
        if node == self.root_list:
            self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left

    def _remove_from_child_list(self, parent, node):
        """Remove um nó específico da lista de filhos de um pai (parent)."""
        if parent.child == parent.child.right:
            parent.child = None  # Era o único filho
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left