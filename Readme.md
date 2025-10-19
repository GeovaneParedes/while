# 🏪 Sistema de Controle de Estoque de Mercadorias

Este projeto implementa um controle simples de **registro** e **retirada de mercadorias**, ideal para ambientes de pequeno porte ou protótipos de gestão de estoque local.

São dois módulos principais:

- **`registro_mercadoria.py`** – Responsável por registrar novos produtos.
- **`abastecimento_mercado.py`** – Responsável por gerenciar retiradas e registrar movimentações de estoque.

---

## 📁 Estrutura de Arquivos

.
├── registro_mercadoria.py # Registro inicial de mercadorias
├── abastecimento_mercado.py # Controle de retiradas / movimentações
├── registro_mercadoria.txt # Armazena registros principais (JSONL)
└── movimentacoes_estoque.txt # Armazena histórico de retiradas

---

## ⚙️ Requisitos

- Python **3.11+**
- Nenhuma dependência externa (somente bibliotecas padrão)

---

## 🚀 Execução Rápida

### 1. Registrar mercadorias

Executa um assistente interativo para cadastrar um produto no estoque:

```bash
python registro_mercadoria.py

Exemplo de uso:

Digite o código da mercadoria: P123
Digite a descrição da mercadoria: Arroz Tipo 1
Digite a quantidade da mercadoria: 50
Digite a validade da mercadoria (DD/MM/AAAA): 30/12/2025
Digite o preço da mercadoria: 5.99

✅ Saída esperada:

Mercadoria registrada com sucesso:
Estoque atual: produto Arroz Tipo 1, validade 30/12/2025, unidades 50.
Registro salvo com sucesso no arquivo.

O arquivo registro_mercadoria.txt será criado (ou atualizado) com uma linha JSON para cada mercadoria registrada:

{"codigo": "P123", "descricao": "Arroz Tipo 1", "quantidade": 50, "validade_produto": "30/12/2025", "preco": 5.99}

2. Retirar mercadorias do estoque

Executa uma interface de retirada interativa:

python abastecimento_mercado.py

Exemplo de uso:

Código do produto: P123
Quantidade a retirar: 5
Nome do funcionário: João

✅ Saída esperada:

Retirada efetuada. Saldo atual: 45 unidades.

Cada retirada gera:

Atualização do arquivo registro_mercadoria.txt (saldo atualizado);

Registro da movimentação no arquivo movimentacoes_estoque.txt:

{"codigo": "P123", "operacao": "retirada", "quantidade_retirada": 5, "saldo_apos": 45, "funcionario": "João", "timestamp": "2025-10-19T14:22:10Z"}

🧩 Funções Principais
registro_mercadoria(codigo, descricao, quantidade, validade_produto, preco) -> dict

Registra uma nova mercadoria no formato de dicionário Python.

| Parâmetro          | Tipo    | Descrição                    |
| ------------------ | ------- | ---------------------------- |
| `codigo`           | `str`   | Código único da mercadoria   |
| `descricao`        | `str`   | Nome/descrição do produto    |
| `quantidade`       | `int`   | Quantidade inicial           |
| `validade_produto` | `str`   | Data no formato `DD/MM/AAAA` |
| `preco`            | `float` | Valor unitário               |

retirar_estoque(codigo_produto, quantidade, funcionario=None, matricula=None, motivo=None)

Gerencia a retirada de itens, atualiza o saldo e registra a movimentação.

Retorno:

(True, registro_atualizado) em sucesso

(False, mensagem) em caso de erro (ex: saldo insuficiente)

🧾 Logs e Auditoria

registro_mercadoria.txt → Contém o estoque atual (cada linha é um registro JSON).

movimentacoes_estoque.txt → Contém o histórico completo de retiradas com timestamps ISO8601.

Esses arquivos podem ser versionados, importados para bancos de dados ou integrados com sistemas maiores.

🔒 Boas Práticas Implementadas

Cada registro e movimentação gravado em formato JSON Lines para facilitar parsing e integração.

Controle de erros em entradas de dados e parsing JSON.

Persistência de dados idempotente (não duplica registros em atualizações).

Estrutura modular e funções reutilizáveis.

Logs de movimentações com timestamp UTC (ISO8601).

🧪 Exemplo de Uso via Script

Você pode importar as funções para uso em outro módulo Python:

from registro_mercadoria import registro_mercadoria
from abastecimento_mercado import retirar_estoque

# Registrar novo produto
produto = registro_mercadoria("A101", "Feijão Carioca", 100, "15/12/2025", 7.50)
print(produto)

# Retirar itens do estoque
ok, info = retirar_estoque("A101", 10, funcionario="Maria")
if ok:
    print(f"Retirada ok, saldo atual: {info['quantidade']}")
else:
    print("Erro:", info)

📦 Próximos Passos (Sugestões de Evolução)

🔄 Conversão para persistência em SQLite (evita concorrência de gravação).

🧍 Integração com autenticação de usuários (funcionários).

🧰 Interface Web ou CLI estruturada (ex: Typer, Rich, FastAPI).

📈 Relatórios automáticos de movimentação por período.

Autor: Equipe de Desenvolvimento
Versão: 1.0.0
Data: 19/10/2025
Licença: MIT
