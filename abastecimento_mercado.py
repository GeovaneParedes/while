import os
import json
from datetime import datetime

REG_FILE = os.path.join(os.path.dirname(__file__), "registro_mercadoria.txt")
MOV_FILE = os.path.join(os.path.dirname(__file__), "movimentacoes_estoque.txt")

def _load_registros():
    if not os.path.exists(REG_FILE):
        return []
    registros = []
    with open(REG_FILE, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            try:
                registros.append(json.loads(linha))
            except Exception:
                continue
    return registros

def _save_registros(registros):
    # sobrescreve o arquivo com o estado atual (um registro por linha JSON)
    with open(REG_FILE, "w", encoding="utf-8") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def _log_movimentacao(mov):
    # grava histórico de movimentações (append) sem alterar o registro principal
    with open(MOV_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(mov, ensure_ascii=False) + "\n")

def retirar_estoque(codigo_produto: str, quantidade: int, funcionario: str = None, matricula: str = None, motivo: str = None):
    """
    Remove `quantidade` do produto `codigo_produto` e sobrescreve o arquivo
    com o novo estado (evita duplicidade de registros).
    Registra também quem solicitou a retirada em arquivo de movimentações.

    Retorna (True, registro_atualizado) em sucesso ou (False, mensagem) em erro.
    """
    if quantidade <= 0:
        return False, "Quantidade deve ser maior que zero."

    registros = _load_registros()
    for idx, reg in enumerate(registros):
        if reg.get("codigo") == codigo_produto:
            try:
                saldo = int(reg.get("quantidade", 0))
            except Exception:
                return False, "Quantidade atual inválida no registro."

            if quantidade > saldo:
                return False, "Saldo insuficiente."

            registros[idx]["quantidade"] = saldo - quantidade
            _save_registros(registros)

            movimento = {
                "codigo": codigo_produto,
                "operacao": "retirada",
                "quantidade_retirada": quantidade,
                "saldo_apos": registros[idx]["quantidade"],
                "funcionario": funcionario,
                "timestamp": datetime.now().isoformat() + "Z"
            }
            _log_movimentacao(movimento)

            return True, registros[idx]

    return False, "Produto não encontrado."

def abastecimento_mercado(codigo_produto: str, quantidade: int):
    sucesso, resultado = retirar_estoque(codigo_produto, quantidade)
    if not sucesso:
        print(f"Falha: {resultado}")
        return False
    print(f"Retirada efetuada. Saldo atual do produto {codigo_produto}: {resultado['quantidade']} unidades.")
    return True

def solicitar_retirada_interativa():
    codigo = input("Código do produto: ").strip()
    try:
        quantidade = int(input("Quantidade a retirar: ").strip())
    except ValueError:
        print("Quantidade inválida.")
        return
    funcionario = input("Nome do funcionário: ").strip()
    

    sucesso, resultado = retirar_estoque(
        codigo,
        quantidade,
        funcionario=funcionario or None,
        )
    if not sucesso:
        print("Falha:", resultado)
    else:
        print(f"Retirada efetuada. Saldo atual: {resultado['quantidade']} unidades.")

if __name__ == "__main__":
    solicitar_retirada_interativa()