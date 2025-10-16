while True:
    num_1, num_2 = int(input("Digite um número: ", "Digite outro número: "))
    operação = input("Digite a operação (+, -, *, /): ")
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
