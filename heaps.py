"""Implemente as três filas de prioridade sem usar heapq."""

from __future__ import annotations


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
    def __init__(self):
        raise NotImplementedError

    def push(self, vertex: int, priority: float):
        raise NotImplementedError

    def decrease_key(self, handle, new_priority: float) -> None:
        raise NotImplementedError

    def pop_min(self) -> tuple[int, float]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


class FibonacciHeap:
    def __init__(self):
        raise NotImplementedError

    def push(self, vertex: int, priority: float):
        raise NotImplementedError

    def decrease_key(self, handle, new_priority: float) -> None:
        raise NotImplementedError

    def pop_min(self) -> tuple[int, float]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

