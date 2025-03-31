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

Menu = '''
[D] Depositar
[S] Sacar
[E] Extrato
[L] Sair

'''

Saldo = 0
Limite = 500
Extrato = ''
Numero_saques = 0
LIMITE_SAQUES = 3

while True:
    os.system('cls')
    print('Bem Vindo ao Sistema Bancário')
    

    print (Menu)
    opcao = input('Informe a opção: ')
    
    
    if opcao == 'D':
        valor = float(input('Digite o valor do deposito: '))
        if valor > 0:
            Saldo += valor
            Extrato += f'Deposito: R${valor:.2f}\n'
            
            print(f'Valor depositado {valor}')
        else:
            print('Falha na operação, o valor informado é invalido')
            time.sleep(4)

    elif opcao == 'S':
        valor_s = float(input('informe o valor do saque: '))

        maior_saldo = valor_s > Saldo
        maior_limite = valor_s > Limite
        maior_saque = Numero_saques >= LIMITE_SAQUES
        
        if maior_saldo:
            print('Operação invalida, saldo insuficiente')
            time.sleep(45)
        elif maior_limite:
            print('Operação invalida, você exedeu o limite')
            time.sleep(4)
        elif maior_saque:
            print('Operação invalida, você exedeu o numero de saque')
            time.sleep(4)
            
        
        elif valor_s > 0:
            Saldo -= valor_s
            Extrato += f'Deposito: R${valor_s:.2f}\n'
            Numero_saques += 1

            print(f'Valor sacado {valor_s}')
            time.sleep(4)
        

        else:
            print('Operação falhou, valor invalido')
            time.sleep(10)

    elif opcao == 'E':
        print("============EXTRATO============")
        print("Não foram realizadas transações" if not Extrato else Extrato)
        print(f'Numero de Saques: {Numero_saques}')
        print(f"Valor do saque: {valor_s*Numero_saques}")
        print(f'Seu saldo é: R$ {Saldo:.2f}')
        time.sleep(10)
    
    elif opcao == 'L':
        print('Você saiu da operação')
        break
    else:
        print('Operação invalida, selecione novamente a opção para a operação')
        time.sleep(10)
              
        