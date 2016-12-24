#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# RUNTIME: Python 3.5.2
# pylint: disable=C0103
# pylint: disable=C0325

""" Main script to simulate some kind of ATM (Automatic Teller Machine). """

from getpass import getpass
from atm import Persistence

d_manager = Persistence()
logged_user = None

print('CAIXA ELETRÔNICO')
print('Hi, hi, Puffy AmiYumi!!!')

print('')

print('Usuários built-in...')
print('-> Agência A1:')
print('Conta: 00000-0 | Senha: pass0')
print('Conta: 11111-1 | Senha: pass1')
print('-> Agência A2')
print('Conta: 22222-2 | Senha: pass2')
print('Conta: 44444-4 | Senha: pass4')
print('-> Agência A3')
print('Conta: 33333-3 | Senha: pass3')

print('')

print('Acesse agora.')
for i in range(0, 3):
    print('')
    agency = input('Agência: ')
    account = input('Conta: ')
    password = getpass('Senha: ')

    trying_user = d_manager.find_user(agency=agency, account=account)

    if trying_user is not None:
        if trying_user.log_in(password):
            logged_user = trying_user
            print('Usuário autorizado.')
            break
        else:
            print('Senha incorreta.')
    else:
        print('Usuário não encontrado.')

if logged_user is None:
    print('\nTentativas esgotadas. Adeus!')
    exit(666)
else:
    print('\nBem-vindo...')

while True:
    print('''
SELECIONE UMA OPERAÇÃO
1 - Saldo       4 - Saque
2 - Extrato     5 - Transferência
3 - Depósito    6 - Sair
    ''')
    op = input(': ')
    print('')
    #print(150 * '\n') # to clear the terminal

    if op[0] == '1': # balance
        print('SALDO:\nR$' + str(logged_user.get_balance()))

    elif op[0] == '2': # history
        print('EXTRATO:')
        for register in logged_user.get_history():
            print(register[0])

    elif op[0] == '3': # deposit
        print('DEPÓSITO.')
        amount = float(input('Quantia: R$').replace(',', '.'))

        to_another_user = input('Na própria conta? (y/n): ')[0]
        to_another_user = not((to_another_user == 'y') or (to_another_user == 'Y'))

        if to_another_user:
            print('Dados do outro usuário...')
            another_user_agency = input('Agência: ')
            another_user_account = input('Conta: ')
            another_user = d_manager.find_user(another_user_agency, another_user_account)
            if another_user is not None:
                logged_user.deposit(amount, another_user)
                print('Depósito realizado na conta fornecida acima.')
            else:
                print('Usuário não encontrado.')
        else:
            logged_user.deposit(amount)
            print('Depósito realizado em sua conta.')


    elif op[0] == '4': # withdraw
        print('SAQUE.')
        print('OBS: disponíveis apenas notas de R$100, R$50 e R$20.')
        print('OBS2: saque máximo de R$1000,00 por vez.')
        amount = float(input('Quantia: R$').replace(',', '.'))

        print('Tentando obter opções de notas para saque...')
        options = logged_user.options_to_withdraw(amount)
        if options is None:
            print('Esse saque não pôde se realizado.')
            print('Verifique seu saldo e a as formas de saque disponíveis.')
        else:
            for i in range(0, len(options)):
                option = options[i]
                qtt_100s, qtt_50s, qtt_20s = (option[0], option[1], option[2])
                print('Opção ' + str(i+1) + ':')
                if qtt_100s > 0:
                    print('\t' + str(qtt_100s) + 'x R$100')
                if qtt_50s > 0:
                    print('\t' + str(qtt_50s) + 'x R$50')
                if qtt_20s > 0:
                    print('\t' + str(qtt_20s) + 'x R$20')
                i += 1

            option = options[int(input('Sua opção: ')) - 1]
            print('Tentando sacar...')
            qtt_100s, qtt_50s, qtt_20s = (option[0], option[1], option[2])

            if logged_user.withdraw_cash(qtt_100s, qtt_50s, qtt_20s):
                print('Fornecidos {}x R$100, {}x R$50 e {}x R$20.'
                      .format(qtt_100s, qtt_50s, qtt_20s))
                print('Saque efetuado com sucesso.')
            else:
                print('Ocorreu algum erro e o saque não foi efetuado.')

    elif op[0] == '5': # transfer
        print('TRANSFERÊNCIA.')
        print('Dados do outro usuário...')
        another_user_agency = input('Agência: ')
        another_user_account = input('Conta: ')
        another_user = d_manager.find_user(another_user_agency, another_user_account)

        if another_user is not None:
            amount = float(input('Quantia: R$').replace(',', '.'))

            if logged_user.transfer_to(amount, another_user):
                print('Transferência realizada com sucesso.')
            else:
                print('Falha ao tentar transferir. Saldo insuficiente?')
        else:
            print('Usuário não encontrado.')

    elif op[0] == '6': # logout
        print('SAIR')
        logged_user.log_out()
        print('Sessão finalizada com sucesso. Saindo...')
        print('Tchau!')
        exit(0)

    else:
        print('Opção inválida.')

    print('')
    input('Digite Enter para salvar as alterações e voltar...')
    d_manager.update_users()
    print('Pronto! Retornando agora.')
