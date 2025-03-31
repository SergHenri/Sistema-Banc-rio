import textwrap  # Importa o módulo textwrap para formatação de texto.
from abc import ABC, abstractclassmethod, abstractproperty  # Importa classes abstratas para criar classes base.
from datetime import datetime, timezone  # Importa classes para trabalhar com datas e horas.
from pathlib import Path  # Importa a classe Path para manipulação de caminhos de arquivos.
import os  # Importa o módulo os para interagir com o sistema operacional.
import json  # Importa o módulo json para trabalhar com arquivos JSON.

ROOT_PATH = Path('.')  # Define o caminho raiz como o diretório atual.
DATA_FILE = ROOT_PATH / "banco_dados.json"  # Define o caminho do arquivo JSON de dados.

def salvar_dados(clientes, contas):
    try:
        dados = {
            "clientes": [
                {
                    "nome": cliente.nome,
                    "cpf": cliente.cpf,
                    "data_nascimento": cliente.data_nascimento,
                    "endereco": cliente.endereco,
                    "contas": [
                        {
                            "numero": conta.numero,
                            "agencia": conta.agencia,
                            "saldo": conta.saldo
                        } for conta in cliente.contas
                    ]
                } for cliente in clientes
            ],
            "contas": [
                {
                    "numero": conta.numero,
                    "agencia": conta.agencia,
                    "saldo": conta.saldo,
                    "cliente": conta.cliente.nome  # ou qualquer outra informação que você queira
                } for conta in contas
            ]
        }

        with open(DATA_FILE, "w", encoding="utf-8") as f:  # Abre o arquivo JSON para escrita.
            json.dump(dados, f, indent=4, ensure_ascii=False)  # Escreve os dados no arquivo JSON.

        print("Dados salvos com sucesso!")

    except Exception as e:
        print(f"Erro ao salvar JSON: e{e}")

def carregar_dados():
    try:
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:  # Verifica se o arquivo existe e não está vazio.
            with open(DATA_FILE, "r") as f:  # Abre o arquivo JSON para leitura.
                dados = json.load(f)  # Carrega os dados do arquivo JSON.

            clientes = []
            for cliente_data in dados.get("clientes", []):  # Itera sobre os dados dos clientes.
                cliente = PessoaFisica(
                    nome=cliente_data["nome"],
                    cpf=cliente_data["cpf"],
                    data_nascimento=cliente_data["data_nascimento"],
                    endereco=cliente_data["endereco"]
                )
                cliente.contas = []  # Inicializa a lista de contas do cliente
                clientes.append(cliente)

            contas = []
            for conta_data in dados.get("contas", []):  # Itera sobre os dados das contas.
                # Encontra o cliente correspondente para associar à conta
                cliente = next((c for c in clientes if c.nome == conta_data["cliente"]), None)
                if cliente:
                    conta = ContaCorrente(
                        numero=conta_data["numero"],
                        cliente=cliente,
                        limite=500,  # Você pode precisar armazenar isso no JSON também
                        limite_saques=50  # Você pode precisar armazenar isso no JSON também
                    )
                    conta._saldo = conta_data["saldo"]
                    contas.append(conta)
                    cliente.contas.append(conta)  # Adiciona a conta à lista de contas do cliente

            return clientes, contas
        else:
            print("Arquivo vazio ou inexistente.")
            return [], []
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return [], []
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON.")
        return [], []
    except Exception as e:
        print(f"Erro inesperado ao carregar dados: {e}")
        return [], []

#--------------------------------------

class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
                Agência:\t{conta.agencia}
                Número:\t\t{conta.numero}
                Titular:\t{conta.cliente.nome}
                Saldo:\t\tR$ {conta.saldo:.2f}
            """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.nome}', '{self.cpf}')>"


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now(timezone.utc).date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
        with open(ROOT_PATH / "log.txt", "a") as arquivo:
            arquivo.write(
                f"[{data_hora}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}. "
                f"Retornou {resultado}\n"
            )
        return resultado

    return envelope


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


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

    # if not cliente.contas:
    #     print("\n@@@ Cliente não possui conta! @@@")
    #     return None  # Retorna None para indicar que o cliente não tem conta

    # if len(cliente.contas) == 1:
    #     return cliente.contas[0]  # Se tiver apenas uma conta, retorna ela

    # print("\nSelecione a conta:")
    # for i, conta in enumerate(cliente.contas):
    #     print(f"{i + 1}. Conta {conta.numero}")

    # while True:
    #     try:
    #         escolha = int(input("Digite o número da conta: ")) - 1
    #         if 0 <= escolha < len(cliente.contas):
    #             return cliente.contas[escolha]  # Retorna a conta escolhida
    #         else:
    #             print("Número de conta inválido.")
    #     except ValueError:
    #         print("Entrada inválida. Digite um número.")


@log_transacao
def depositar(clientes, valor):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    transacao = Deposito(valor)


    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
    return f"Depósito de {valor} realizado com sucesso!"


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, limite=500, limite_saques=50)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes, contas = carregar_dados()
    if clientes is None or contas is None:
        print("Erro ao carregar dados.")
        return

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            depositar(clientes, valor)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)
            salvar_dados(clientes, contas)  # Salva após criar um novo usuário

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
            salvar_dados(clientes, contas)  # Salva após criar uma nova conta

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()