from heaps import BinaryHeap

def test_binary_heap():
    print("Testes da BinaryHeap")
    
    bh = BinaryHeap()
    print(f"Tamanho inicial: {len(bh)} (Esperado: 0)")

    print("\n1 Testando Inserção (push)")
    bh.push(vertex=1, priority=10.0)
    bh.push(vertex=2, priority=5.0)
    bh.push(vertex=3, priority=15.0)
    bh.push(vertex=4, priority=1.0)
    print(f"Tamanho após 4 inserções: {len(bh)} (Esperado: 4)")

    print("\n2 Testando pop_min")
    print("Extraindo o mínimo, esperado: Vértice 4 (prioridade 1.0)")
    v, p = bh.pop_min()
    print(f"Resultado Vértice: {v}, Prioridade: {p}")

    print("\n3 Testando decrease_key")
    # Estado atual aproximado: (2, 5.0), (1, 10.0), (3, 15.0)
    
    # Inserind um novo vértice com prioridade alta
    handle_5 = bh.push(vertex=5, priority=20.0)
    print(f"Vértice 5 inserido com prioridade: {handle_5.priority}")
    
    print("Diminuindo a prioridade do vértice 5 de 20.0 para 2.0")
    bh.decrease_key(handle_5, 2.0)
    
    print("Mmínimo. Esperado: Vértice 5 (prioridade 2.0)")
    v, p = bh.pop_min()
    print(f"Resultado Vértice: {v}, Prioridade: {p}")


    print("\n4 Esvaziando o restante da heap (Ordem esperada: 5.0, 10.0, 15.0)")
    while len(bh) > 0:
        v, p = bh.pop_min()
        print(f"Removido Vértice: {v}, Prioridade: {p}")

    print("\n5 Testando exceções")
    
    try:
        bh.pop_min()
        print("ERRO: Deveria ter lançado IndexError")
    except IndexError as e:
        print(f"Sucesso ao bloquear fila vazia: '{e}'")


    handle_6 = bh.push(vertex=6, priority=10.0)
    try:
        bh.decrease_key(handle_6, 15.0)
        print("ERRO: Deveria ter lançado ValueError")
    except ValueError as e:
        print(f"Sucesso ao bloquear aumento de prioridade: '{e}'")

    print("\nodos os testes concluídos")

if __name__ == '__main__':
    test_binary_heap()