"""Operação de depósito

Deve ser possível depositar valores positivos para a minha
conta bancária. A v1 do projeto trabalha apenas com 1 usuário,
dessa forma não precisamos nos preocupar em identificar qual
é o número da agência e conta bancária. Todos os depósitos
devem ser armazenados em uma variável e exibidos na
operação de extrato."""

"""Operação de saque

O sistema deve permitir realizar 3 saques diários com limite
máximo de R$ 500,00 por saque. Caso o usuário não tenha
saldo em conta, o sistema deve exibir uma mensagem
informando que não será possível sacar o dinheiro por falta de
saldo. Todos os saques devem ser armazenados em uma
variável e exibidos na operação de extrato."""

"""Operação de extrato

Essa operação deve listar todos os depósitos e saques
realizados na conta. No fim da listagem deve ser exibido o
saldo atual da conta.

Os valores devem ser exibidos utilizando o formato R$ xxx.xx,
exemplo:

1500.45 = R$ 1500.45"""

import os
import time

# Menu de opções
Menu = '''
[D] Depositar
[S] Sacar
[E] Extrato
[L] Sair
'''

# Inicialização de variáveis
Saldo = 0  # Saldo inicial da conta
Limite = 500  # Limite máximo para saques
Extrato = ''  # Armazena o histórico de transações
Numero_saques = 0  # Contador de saques realizados
LIMITE_SAQUES = 3  # Limite de saques permitidos

while True:
    os.system('cls')  # Limpa a tela (Windows)
    print('Bem Vindo ao Sistema Bancário')
    
    # Exibe o menu de opções
    print(Menu)
    opcao = input('Informe a opção: ')
    
    # Opção de depósito
    if opcao == 'D':
        valor = float(input('Digite o valor do deposito: '))  # Solicita o valor para depósito
        if valor > 0:  # Verifica se o valor é válido
            Saldo += valor  # Atualiza o saldo com o valor depositado
            Extrato += f'Deposito: R${valor:.2f}\n'  # Adiciona o depósito ao extrato
            
            print(f'Valor depositado {valor}')
        else:
            print('Falha na operação, o valor informado é invalido')
            time.sleep(4)  # Aguarda 4 segundos para o usuário ler a mensagem

    # Opção de saque
    elif opcao == 'S':
        valor_s = float(input('informe o valor do saque: '))  # Solicita o valor para saque

        # Verificação de condições para o saque
        maior_saldo = valor_s > Saldo  # Verifica se o valor do saque é maior que o saldo
        maior_limite = valor_s > Limite  # Verifica se o valor do saque excede o limite
        maior_saque = Numero_saques >= LIMITE_SAQUES  # Verifica se o número de saques excedeu o limite

        # Mensagens de erro conforme a verificação das condições
        if maior_saldo:
            print('Operação invalida, saldo insuficiente')
            time.sleep(4)  # Aguarda 4 segundos para o usuário ler a mensagem
        elif maior_limite:
            print('Operação invalida, você excedeu o limite')
            time.sleep(4)
        elif maior_saque:
            print('Operação invalida, você excedeu o número de saques')
            time.sleep(4)
        elif valor_s > 0:  # Verifica se o valor do saque é válido
            Saldo -= valor_s  # Atualiza o saldo com o valor do saque
            Extrato += f'Saque: R${valor_s:.2f}\n'  # Adiciona o saque ao extrato
            Numero_saques += 1  # Incrementa o contador de saques

            print(f'Valor sacado {valor_s}')
            time.sleep(4)

        else:
            print('Operação falhou, valor invalido')  # Caso o valor do saque seja inválido
            time.sleep(4)

    # Opção de extrato
    elif opcao == 'E':
        print("============EXTRATO============")
        print("Não foram realizadas transações" if not Extrato else Extrato)  # Exibe o extrato ou mensagem caso não haja transações
        print(f'Número de Saques: {Numero_saques}')  # Exibe o número de saques realizados
        print(f"Valor do saque: R${valor_s*Numero_saques:.2f}")  # Exibe o total sacado
        print(f'Seu saldo é: R$ {Saldo:.2f}')  # Exibe o saldo atual
        time.sleep(10)

    # Opção de sair
    elif opcao == 'L':
        print('Você saiu da operação')  # Mensagem de saída
        break  # Encerra o loop e sai do programa

    # Opção inválida
    else:
        print('Operação invalida, selecione novamente a opção para a operação')  # Mensagem de erro para operação inválida
        time.sleep(10)  # Aguarda 10 segundos para o usuário ler a mensagem
