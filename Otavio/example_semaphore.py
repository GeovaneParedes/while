#!/usr/bin/env python3
"""
Exemplo: semaforo (12), threads que adquirem/release e tratamento de KeyboardInterrupt.

Como usar:
    python example_semaphore.py

Requisitos:
    Python 3.11+

O comportamento demonstra:
 - um Semaphore com contador máximo 12
 - threads adquirem o semáforo, simulam trabalho (I/O/CPU)
 - GIL: observe que apenas uma thread executa bytecode Python por vez no CPython,
   mas o semáforo controla simultaneidade lógica do recurso
 - captura de KeyboardInterrupt para término ordenado
"""

from threading import Thread, Semaphore, Event
import time
import random
import sys

MAX_CONCURRENT = 12
WORKER_COUNT = 30  # número de threads que queremos tentar executar
RUN_TIME_SEC = 0.15  # tempo de "trabalho" de cada thread (simulado)


def worker(i: int, sem: Semaphore, stop_event: Event) -> None:
    """
    Função de trabalho de cada thread.

    Parâmetros:
        i: índice da thread (int)
        sem: semáforo compartilhado (Semaphore)
        stop_event: evento que sinaliza parada (Event)
    """
    # tenta adquirir o semáforo, com timeout para conseguir responder a stop_event
    acquired = False
    try:
        while not stop_event.is_set():
            # tenta adquirir por um curto período para poder checar o stop_event
            acquired = sem.acquire(timeout=0.1)
            if not acquired:
                # volta ao loop e checa se deve parar
                continue
            # se adquiriu, simula trabalho
            print(f"[T{i}] acquired; trabalhando...")
            # simula variação (I/O bound ou CPU curto)
            time.sleep(RUN_TIME_SEC + random.random() * RUN_TIME_SEC)
            print(f"[T{i}] done; releasing.")
            sem.release()
            return
    except Exception as e:
        # log simples para debugging; não suprime KeyboardInterrupt/control flow externo
        print(f"[T{i}] exceção: {e!r}")
    finally:
        # se o loop terminou por stop_event mas semaforo ficou adquirido, soltar
        if acquired:
            try:
                sem.release()
            except Exception:
                pass


def main() -> int:
    """
    Cria threads e um semáforo com capacidade MAX_CONCURRENT.
    Captura KeyboardInterrupt para parada ordenada.
    Retorna código de saída (0 sucesso, 1 interrupção).
    """
    sem = Semaphore(MAX_CONCURRENT)
    stop_event = Event()
    threads = []

    # Criar threads
    for i in range(WORKER_COUNT):
        t = Thread(target=worker, args=(i, sem, stop_event), daemon=True)
        threads.append(t)

    # Start em lote (não precisamos iniciar tudo de uma vez necessariamente)
    for t in threads:
        t.start()

    try:
        # Mantém o main vivo enquanto threads terminam; em produção
        # pode-se usar join() com timeout e checar stop_event
        while any(t.is_alive() for t in threads):
            time.sleep(0.2)
    except KeyboardInterrupt:
        # Ctrl+C: sinaliza parada e aguarda liberação
        print("\nKeyboardInterrupt recebido: sinalizando threads para encerrarem...")
        stop_event.set()
        # Opcional: aguarda um tempo prudente para limpeza
        grace = 3.0
        t0 = time.time()
        for t in threads:
            remaining = max(0.0, grace - (time.time() - t0))
            t.join(timeout=remaining)
        # Após grace period, threads daemon terminarão com o processo
        print("Parada ordenada concluída (ou timeout).")
        return 1

    # Verificações simples (testes)
    # nenhuma thread deve manter o semáforo bloqueado além do esperado:
    # como utilizamos release sempre que adquirimos, contador volta a MAX_CONCURRENT
    # Esse assert é um check heurístico: tentamos adquirir MAX_CONCURRENT vezes sem bloquear.
    acquired_now = []
    for _ in range(MAX_CONCURRENT):
        if sem.acquire(blocking=False):
            acquired_now.append(True)
        else:
            acquired_now.append(False)
    # restaurar o semáforo ao estado original
    for _ in acquired_now:
        sem.release()
    # Todos os acquires não-bloqueantes deveriam ter sido bem-sucedidos
    assert all(acquired_now), "Semáforo final não retornou ao estado máximo esperado."

    print("Execução concluída normalmente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

