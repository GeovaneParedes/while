# 🧵 Example Semaphore — Controle de Concorrência em Python

![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Stable-success.svg)

Exemplo didático e **100% funcional** de uso de `threading.Semaphore` em Python,  
com controle de concorrência, respeito ao **GIL (Global Interpreter Lock)**  
e tratamento limpo de interrupções (`KeyboardInterrupt`).

---

## 🚀 Visão Geral

Este script demonstra como limitar o número de threads que executam simultaneamente  
uma seção crítica, utilizando um **semáforo**.  

O exemplo cria 30 threads, mas apenas **12** podem “entrar no banheiro” (isto é,  
executar a seção protegida) ao mesmo tempo.

> 🧠 Analogia: imagine uma grande festa com um único banheiro e uma única **chave GIL**.  
> Cada pessoa (thread) precisa pegar a chave (`acquire`), usar o banheiro e devolvê-la (`release`)  
> para a próxima pessoa na fila. Assim funciona a execução de bytecode sob o GIL em CPython.

---

## 📂 Estrutura

example_semaphore.py
README.md

---

## 🧩 Principais Conceitos Demonstrados

- `threading.Semaphore` e controle de simultaneidade (`MAX_CONCURRENT = 12`)
- Bloqueio e liberação explícita (`acquire()` / `release()`)
- Comunicação segura entre threads usando `threading.Event`
- Tratamento de `KeyboardInterrupt` para encerramento ordenado
- Garantia de liberação de recursos mesmo em exceções
- Assert de sanidade para validar o estado final do semáforo
- Demonstração prática do **GIL (Global Interpreter Lock)**

---

## ⚙️ Requisitos

- **Python 3.11+**
- Nenhuma dependência externa

---

## ▶️ Como Executar

```bash
python example_semaphore.py

Saída esperada (aproximada):

[T0] acquired; trabalhando...
[T1] acquired; trabalhando...
[T2] acquired; trabalhando...
...
[T5] done; releasing.
[T13] acquired; trabalhando...
Execução concluída normalmente.

Durante a execução, pressione Ctrl+C para testar o tratamento de interrupção:

KeyboardInterrupt recebido: sinalizando threads para encerrarem...
Parada ordenada concluída (ou timeout).

🧪 Teste Integrado

O próprio script inclui um teste simples de sanidade:

assert all(acquired_now), "Semáforo final não retornou ao estado máximo esperado."

Esse teste garante que todos os release() foram chamados corretamente
e o semáforo voltou ao estado inicial (MAX_CONCURRENT).

🧱 Explicação Técnica Rápida

GIL (Global Interpreter Lock): trava global da VM CPython que garante
que apenas uma thread execute bytecode Python por vez.
Isso não impede concorrência I/O-bound, mas limita o paralelismo CPU-bound.

Semaphore: estrutura de sincronização que mantém um contador interno.
Cada acquire() decrementa o contador; cada release() o incrementa.
Se o contador chega a zero, threads seguintes bloqueiam até alguém liberar.

KeyboardInterrupt (Ctrl+C): é capturado pela main thread e usado aqui
para sinalizar (Event.set()) que todas as threads devem encerrar com segurança.

🧠 Aprendizados-Chave

O GIL não substitui locks do usuário — ele só protege o interpretador.

Use Semaphore para limitar acesso a recursos compartilhados (como conexões, arquivos ou jobs paralelos).

Sempre trate interrupções e libere recursos de forma explícita.

Concorrência ≠ Paralelismo.

🧾 Licença

Distribuído sob a licença MIT — veja o arquivo LICENSE

✍️ Autor

Desenvolvido por @DevGege
Inspirado nas aulas e analogias do professor Otávio Miranda
