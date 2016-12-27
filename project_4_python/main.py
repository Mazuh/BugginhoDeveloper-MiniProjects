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

print('AUTOMATIC TELLER MACHINE')
print('Hi, hi, Puffy AmiYumi!!!')

print('')

print('Users built-in...')
print('-> Agency A1:')
print('Account: 00000-0 | Password: pass0')
print('Account: 11111-1 | Password: pass1')
print('-> Agency A2')
print('Account: 22222-2 | Password: pass2')
print('Account: 44444-4 | Password: pass4')
print('-> Agency A3')
print('Account: 33333-3 | Password: pass3')

print('')

print('Access now.')
for i in range(0, 3):
    print('')
    agency = input('Agency: ')
    account = input('Account: ')
    password = getpass('Password: ')

    trying_user = d_manager.find_user(agency=agency, account=account)

    if trying_user is not None:
        if trying_user.log_in(password):
            logged_user = trying_user
            print('Authorized user.')
            break
        else:
            print('Wrong password.')
    else:
        print('User not found.')

if logged_user is None:
    print('\nAttempts exhausted! Goodbye!')
    exit(666)
else:
    print('\nWelcome...')

while True:
    print('''
Choose an option
1 - Balance       4 - Withdraw
2 - Extract       5 - Transfer
3 - Deposit      6 - Exit
    ''')
    op = input(': ')
    print('')
    #print(150 * '\n') # to clear the terminal

    if op[0] == '1': # balance
        print('BALANCE:\n$' + str(logged_user.get_balance()))

    elif op[0] == '2': # history
        print('EXTRACT:')
        for register in logged_user.get_history():
            print(register[0])

    elif op[0] == '3': # deposit
        print('DEPOSIT.')
        amount = float(input('Amount: $').replace(',', '.'))

        to_another_user = input('In your own account? (y/n): ')[0]
        to_another_user = not((to_another_user == 'y') or (to_another_user == 'Y'))

        if to_another_user:
            print('Other user data...')
            another_user_agency = input('Agency: ')
            another_user_account = input('Account: ')
            another_user = d_manager.find_user(another_user_agency, another_user_account)
            if another_user is not None:
                logged_user.deposit(amount, another_user)
                print('Deposit successfully in the account provided above')
            else:
                print('User not found.')
        else:
            logged_user.deposit(amount)
            print('Deposit successfully in your account.')


    elif op[0] == '4': # withdraw
        print('WITHDRAW.')
        print('OBS: Only $100, $50 and $20 bills are available.')
        print('OBS2: The maximum value you can withdraw is $1000,00.')
        amount = float(input('Amount: $').replace(',', '.'))

        print('Trying to get bills options to withdraw.')
        options = logged_user.options_to_withdraw(amount)
        if options is None:
            print("This withdraw couldn't be held.")
            print('Verify you balance and the withdraw ways available.')
        else:
            for i in range(0, len(options)):
                option = options[i]
                qtt_100s, qtt_50s, qtt_20s = (option[0], option[1], option[2])
                print('Option ' + str(i+1) + ':')
                if qtt_100s > 0:
                    print('\t' + str(qtt_100s) + 'x $100')
                if qtt_50s > 0:
                    print('\t' + str(qtt_50s) + 'x $50')
                if qtt_20s > 0:
                    print('\t' + str(qtt_20s) + 'x $20')
                i += 1

            option = options[int(input('Your option: ')) - 1]
            print('Trying to withdraw...')
            qtt_100s, qtt_50s, qtt_20s = (option[0], option[1], option[2])

            if logged_user.withdraw_cash(qtt_100s, qtt_50s, qtt_20s):
                print('Provided {}x $100, {}x $50 e {}x $20.'
                      .format(qtt_100s, qtt_50s, qtt_20s))
                print('Withdraw successfully.')
            else:
                print("An error occurred and the withdraw couldn't be held.")

    elif op[0] == '5': # transfer
        print('TRANSFER.')
        print('Other user data...')
        another_user_agency = input('Agency: ')
        another_user_account = input('Account: ')
        another_user = d_manager.find_user(another_user_agency, another_user_account)

        if another_user is not None:
            amount = float(input('Amount: $').replace(',', '.'))

            if logged_user.transfer_to(amount, another_user):
                print('Transfer successfully.')
            else:
                print('Transfer failed. Isufficient balance?')
        else:
            print('User not found.')

    elif op[0] == '6': # logout
        print('EXIT')
        logged_user.log_out()
        print('Section closed. Exiting...')
        print('Bye Bye!')
        exit(0)

    else:
        print('Invalid option.')

    print('')
    input('Press Enter to save the changes and go back...')
    d_manager.update_users()
    print('Ok! Returning now.')
