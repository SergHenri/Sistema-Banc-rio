# Separar as funções existentes de saque, depósito e extrato em funções.  
# Criar duas novas funções: cadastrar usuário (cliente) e cadastrar conta bancária.  

# Menu com as opções disponíveis para o usuário  
menu = '''
    [S] Saque
    [D] Depositar
    [E] Extrato
    [NC] Nova Conta
    [NU] Novo Usuário
    [LC] Listar Contas
    [Ex] Sair
'''

# Função para realizar um depósito  
# Recebe os argumentos apenas por posição (positional only)
def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor  # Adiciona o valor ao saldo
        extrato += f'Depósito: R$ {valor:.2f}\n'  # Registra a transação no extrato
        print('Depósito realizado com sucesso')
    else:
        print('Valor informado é inválido')

    return saldo, extrato  # Retorna o novo saldo e extrato atualizado

# Função para realizar um saque  
# Os argumentos são passados apenas por nome (keyword only)
def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    maior_saldo = valor > saldo  # Verifica se o saldo é suficiente
    maior_limite = valor > limite  # Verifica se o saque não excede o limite permitido
    maior_saque = numero_saques >= limite_saques  # Verifica se o número de saques diários foi atingido

    if maior_saldo:
        print('Operação falhou, saldo insuficiente')
    
    elif maior_limite:
        print('Operação falhou, saque maior que o limite')

    elif maior_saque:
        print('Operação falhou, você excedeu o limite de saques por dia')

    elif valor > 0:
        saldo -= valor  # Deduz o valor do saldo
        extrato += f'Saque R$: {valor:.2f}\n'  # Registra a transação no extrato
        numero_saques += 1  # Incrementa o número de saques realizados
        print("=== Saque realizado com sucesso! ===")

    else:
        print('Operação falhou, informe um valor válido')

    return saldo, extrato  # Retorna o saldo e extrato atualizados

# Função para exibir o extrato bancário  
# Recebe argumentos por posição e nome (positional only e keyword only)
def exibir_extrato(saldo, *, extrato):
    print('=========== EXTRATO ===========')
    print("Não foram realizadas movimentações." if not extrato else extrato)  # Exibe extrato ou mensagem se não houver movimentações
    print(f"\nSaldo: R$ {saldo:.2f}")  # Exibe o saldo atual
    print("=========== EXTRATO ===========")

# Função para criar um novo usuário  
# O usuário é identificado pelo CPF e deve ser único
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)  # Verifica se o CPF já está cadastrado

    if usuario:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Adiciona o usuário à lista de usuários
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

# Função auxiliar para buscar um usuário pelo CPF  
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]  # Filtra usuários pelo CPF
    return usuarios_filtrados[0] if usuarios_filtrados else None  # Retorna o usuário se encontrado

# Função para criar uma conta bancária  
# Cada conta possui um número sequencial e é vinculada a um usuário existente
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('=== Conta criada com sucesso! ===')
        return {
            'agencia': agencia,
            'numero_conta': numero_conta,
            'usuario': usuario
        }

    print('Usuário não encontrado')

# Função para listar todas as contas cadastradas  
def listar_contas(contas):
    for conta in contas:  # Percorre a lista de contas cadastradas
        linha = f"""  
            Agência: {conta['agencia']}
            C/C: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print("=" * 100)
        print(linha)

# Função principal para executar o sistema bancário  
def main():
    saldo = 0  # Saldo inicial da conta
    limite = 500  # Limite máximo de saque por operação
    extrato = ""  # Histórico de transações
    numero_saques = 0  # Contador de saques realizados
    usuarios = []  # Lista para armazenar os usuários cadastrados
    contas = []  # Lista para armazenar as contas cadastradas
    LIMITE_SAQUES = 3  # Quantidade máxima de saques diários
    AGENCIA = '0001'  # Número fixo da agência bancária

    while True:
        print('Seja Bem-Vindo ao seu Sistema Bancário\n')
        print(menu)
        opcao = input('Informe a opção: ').strip().upper()  # Captura a opção do usuário

        if opcao == 'D':
            valor = float(input('Digite o valor a ser depositado: '))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 'S':
            valor = float(input('Digite o valor a ser sacado: '))
            saldo, extrato = saque(
                saldo=saldo, 
                valor=valor, 
                extrato=extrato, 
                limite=limite, 
                numero_saques=numero_saques, 
                limite_saques=LIMITE_SAQUES
            )
        
        elif opcao == 'E':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "NU":
            criar_usuario(usuarios)

        elif opcao == 'NC':
            numero_conta = len(contas) + 1  # Gera um número sequencial para a conta
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)  # Adiciona a conta à lista de contas

        elif opcao == "LC":
            listar_contas(contas)

        elif opcao == "EX":
            print("Saindo do sistema... Obrigado por utilizar nosso banco!")
            break  
        
        else:
            print("Operação inválida, por favor selecione novamente a opção desejada.")

# Executa o programa principal  
main()
