def menu():
        menu = """Escolha a operação desejada:
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
-->"""
        return int(input(menu))

def depositar(saldo, valor, extrato, /):
        if(valor > 0):
                saldo += valor
                extrato.append(f"Depósito: R$ {valor:.2f}")
                print(f"Depósito no valor de R$ {valor:.2f} realizado com sucesso\n")
                return saldo, extrato
        else:
                print("Operação não realizada. O valor informado é inválido.\n")
                return None, None

def main():
        boas_vindas = "Bem vindo ao seu sistema bancário!"
        
        saldo = 0
        limite = 500
        extrato = []
        numero_saques = 0
        LIMITE_SAQUES = 3
        
        print(boas_vindas)
        
        while(True):
                opcao = menu()

                if(opcao == 1):
                        valor = float(input("Insira o valor desejado para depositar:"))
                        saldo_atual, extrato_atual = depositar(saldo, valor, extrato) #Para não substituir o 0 inicial pelo None do return caso o valor seja menor que 0
                        if(saldo_atual and extrato_atual): #Se não retornou None atualiza o saldo e o extrato
                                saldo = saldo_atual
                                extrato = extrato_atual
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

main()