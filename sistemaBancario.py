menu = """
        Bem vindo ao Banco Python

    Digite a opção desejada:
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

limite_saque = 500
LIMITE_DIARIO = 3
saque_efetuado = 0
saldo = 0
extrato = ""

while True:
    
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Digite o valor a ser depositado: "))

        if valor > 0:
            extrato += f"Depósito: R$ {valor:.2f}\n"
            saldo += valor
            print("Deposito efetuado com sucesso!")
        else:
            print("Deposito nao efetuado. Digite as informações corretamente. ")

    elif opcao == "s":
        valor_saque = float(input("Digite o valor a ser sacado: "))

        excedeu_saldo = valor_saque > saldo
        excedeu_limite = valor_saque > limite_saque
        excedeu_saques = saque_efetuado >= LIMITE_DIARIO

        if excedeu_saldo:
            print("Voce nao tem saldo disponivel")
        elif excedeu_limite:
            print("Voce nao tem limite maximo pra saque disponivel")
        elif excedeu_saques:
            print("Voce nao tem limite diario disponivel")
        else:
            saldo -= valor_saque
            extrato += f"Saque: R$ {valor:.2f}\n"
            saque_efetuado += 1
            print("Saque efetuado")       

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")