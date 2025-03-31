import os
import time

# Menu de opções
MENU = """
[d] Depositar
[s] Sacar
[e] Extrato
[l] Sair
"""

# Inicialização de variáveis
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
total_sacado = 0 #variavel para armazenar o valor total sacado.

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Valor depositado: R$ {valor:.2f}")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES, total_sacado):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        total_sacado += valor
        print(f"Valor sacado: R$ {valor:.2f}")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques, total_sacado

def exibir_extrato(saldo, extrato, numero_saques, total_sacado):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nNúmero de saques: {numero_saques}")
    print(f"Total sacado: R$ {total_sacado:.2f}")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Bem vindo ao sistema bancário")
    print(MENU)

    opcao = input("Informe a opção desejada: ")

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = depositar(saldo, valor, extrato)
        time.sleep(4)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, numero_saques, total_sacado = sacar(saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES, total_sacado)
        time.sleep(4)

    elif opcao == "e":
        exibir_extrato(saldo, extrato, numero_saques, total_sacado)
        time.sleep(10)

    elif opcao == "l":
        print("Obrigado por utilizar nosso sistema, até logo!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
        time.sleep(4)