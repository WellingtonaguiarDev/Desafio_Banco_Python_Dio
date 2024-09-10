import textwrap

class Transacao:
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.append(f"Depósito:\tR$ {self.valor:.2f}")
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

class Saque(Transacao):
    def __init__(self, valor, limite):
        super().__init__(valor)
        self.limite = limite

    def registrar(self, conta):
        excedeu_saldo = self.valor > conta.saldo
        excedeu_limite = self.valor > self.limite
        excedeu_saques = conta.numero_saques >= conta.limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif self.valor > 0:
            conta.saldo -= self.valor
            conta.historico.append(f"Saque:\t\tR$ {self.valor:.2f}")
            conta.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")


class Conta:
    def __init__(self, agencia, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = []
        self.limite_saques = 3
        self.numero_saques = 0

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.historico else "\n".join(self.historico))
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")


class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuario = Cliente(nome, data_nascimento, cpf, endereco)
    usuarios.append(usuario)
    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = Conta(agencia, numero_conta, usuario)
        usuario.adicionar_conta(conta)
        print("\n=== Conta criada com sucesso! ===")
        return conta

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


# Main

def main():
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do titular da conta: ")
            usuario = filtrar_usuario(cpf, usuarios)
            if usuario:
                valor = float(input("Informe o valor do depósito: "))
                conta = usuario.contas[0]  # Considerando que o cliente tenha uma conta
                deposito = Deposito(valor)
                deposito.registrar(conta)
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "s":
            cpf = input("Informe o CPF do titular da conta: ")
            usuario = filtrar_usuario(cpf, usuarios)
            if usuario:
                valor = float(input("Informe o valor do saque: "))
                conta = usuario.contas[0]
                saque = Saque(valor, 500)
                saque.registrar(conta)
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "e":
            cpf = input("Informe o CPF do titular da conta: ")
            usuario = filtrar_usuario(cpf, usuarios)
            if usuario:
                conta = usuario.contas[0]
                conta.exibir_extrato()
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
