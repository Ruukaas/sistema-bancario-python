menu = """Escolha a operação desejada:
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
-->"""

boas_vindas = "Bem vindo ao seu sistema bancário!"

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

print(boas_vindas)
while(True):
        opcao = int(input(menu))

        if(opcao == 1):
                valor = float(input("Insira o valor desejado para depositar:"))
                if(valor > 0):
                       saldo += valor
                       extrato.append(f"Depósito: R$ {valor:.2f}")
                       print(f"Depósito no valor de R$ {valor:.2f} realizado com sucesso\n")
                else:
                       print("Operação não realizada. O valor informado é inválido.\n")
        elif(opcao == 2):
                valor = float(input("Insira o valor do saque: ")) 
                if(numero_saques >= LIMITE_SAQUES): 
                        print("Operação não realizada. Limite de saques atingido.\n") 
                elif(valor > limite): 
                        print("Operação não realizada. Limite de valor de saque atingido.\n") 
                elif(valor > saldo):
                        print("Operação não realizada. Valor maior que saldo disponível")
                elif(valor > 0): 
                        saldo -= valor
                        numero_saques+=1
                        extrato.append(f"Saque: R$ {valor:.2f}")
                        print(f"Saque no valor de R$ {valor:.2f} realizado com sucesso\n")
                else:
                        print("Operação não realizada. Insira um valor válido\n")
        elif(opcao == 3):
                if(len(extrato) == 0):
                        print("Não foram realizadas movimentações")
                else:
                        print("########## - Extrato - ###############")
                        for indice, entrada in enumerate(extrato):
                                print(f"Entrada {indice+1}: {entrada}")      
                        print(f"\nSaldo atual: R$ {saldo:.2f}")
                        print("######################################")
                print() 
        elif(opcao == 0):
                print("Até logo.")
                break
        else:
                print("Opção inválida, por favor insira uma opção válida")
