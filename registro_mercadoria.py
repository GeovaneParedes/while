import json

def registro_mercadoria(codigo, descricao, quantidade, validade_produto, preco):
    """
    Registra uma mercadoria com os detalhes fornecidos.

    Parâmetros:
    codigo (str): Código único da mercadoria.
    descricao (str): Descrição da mercadoria.
    quantidade (int): Quantidade disponível da mercadoria.
    validade_produto (str): Data de validade no formato DD/MM/AAAA.
    preco (float): Preço unitário da mercadoria.

    Retorna:
    dict: Um dicionário contendo os detalhes da mercadoria registrada.
    """
    mercadoria = {
        "codigo": codigo,
        "descricao": descricao,
        "quantidade": quantidade,
        "validade_produto": validade_produto,
        "preco": preco
    }
    return mercadoria

try:
    codig = input("Digite o código da mercadoria: ").strip()
    desc = input("Digite a descrição da mercadoria: ").strip()
    quant = int(input("Digite a quantidade da mercadoria: ").strip())
    val = input("Digite a validade da mercadoria (DD/MM/AAAA): ").strip()
    prec = float(input("Digite o preço da mercadoria: ").strip())
except ValueError:
    print("Entrada inválida. Quantidade deve ser inteiro e preço deve ser número.")
else:
    mercadoria = registro_mercadoria(codig, desc, quant, val, prec)
    print("Mercadoria registrada com sucesso:")
    print(f"Estoque atual: produto {mercadoria['descricao']}, validade {mercadoria['validade_produto']}, unidades {mercadoria['quantidade']}.")

    # Grava sem apagar registros anteriores — cada mercadoria em uma linha JSON
    with open("registro_mercadoria.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(mercadoria, ensure_ascii=False) + "\n")

    print("Registro salvo com sucesso no arquivo.")
