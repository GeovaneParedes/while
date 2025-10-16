while True:
    try:
        num_1 = int(input("Digite um número: ")) 
        num_2 = int(input("Digite outro número: "))
        operação = input("Digite a operação (+, -, *, /): ")

    except ValueError:
            print("Entrada inválida. Digite números inteiros.")
            continue


    if operação == "+":
        print(f"{num_1} + {num_2} = {num_1 + num_2}")
    elif operação == "-":
        print(f"{num_1} - {num_2} = {num_1 - num_2}")
    elif operação == "*":
        print(f"{num_1} * {num_2} = {num_1 * num_2}")
    elif operação == "/":
        if num_2 != 0:
            print(f"{num_1} / {num_2} = {num_1 / num_2}")
        else:
            print("Erro: Divisão por zero não é permitida.")
    else:
        print("Operação inválida. Tente novamente.")
    continuar = input("Deseja continuar? (s/n): ").lower()
    if continuar != 's':
        break
