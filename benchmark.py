"""Experimento reproduzível; complete e gere os dados do relatório."""

from __future__ import annotations

import random
import statistics
import time

SEED = 2027


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

