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

def sacar(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
        excedeu_limite_saques = numero_saques >= limite_saques
        excedeu_limite_valor_saque = valor > limite
        excedeu_saldo = valor > saldo
        
        if(excedeu_limite_saques): 
                print("Operação não realizada. Limite de saques atingido.\n") 
                return None, None, None
        elif(excedeu_limite_valor_saque): 
                print("Operação não realizada. Limite de valor de saque atingido.\n") 
                return None, None, None
        elif(excedeu_saldo):
                print("Operação não realizada. Valor maior que saldo disponível")
                return None, None, None
        elif(valor > 0): 
                saldo -= valor
                numero_saques+=1
                extrato.append(f"Saque: R$ {valor:.2f}")
                print(f"Saque no valor de R$ {valor:.2f} realizado com sucesso\n")
                return saldo, extrato, numero_saques
        else:
                print("Operação não realizada. Insira um valor válido\n")
                return None, None, None
        
def exibir_extrato(saldo,/,*,extrato):
        if(len(extrato) == 0):
                print("Não foram realizadas movimentações")
        else:
                print("########## - Extrato - ###############")
                for indice, entrada in enumerate(extrato):
                        print(f"Entrada {indice+1}: {entrada}")      
                print(f"\nSaldo atual: R$ {saldo:.2f}")
                print("######################################")
                print() 
                
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
                        saldo_atual_deposito, extrato_atual_deposito = depositar(saldo, valor, extrato) #Para não substituir o 0 inicial pelo None do return caso o valor seja menor que 0
                        if(saldo_atual_deposito and extrato_atual_deposito): #Se não retornou None atualiza o saldo e o extrato
                                saldo = saldo_atual_deposito
                                extrato = extrato_atual_deposito
                elif(opcao == 2):
                        valor = float(input("Insira o valor do saque: ")) 
                        saldo_atual_saque, extrato_atual_saque, numero_saques_atual_saque = sacar(saldo = saldo, 
                                numero_saques = numero_saques, 
                                extrato = extrato, 
                                limite= limite, 
                                limite_saques = LIMITE_SAQUES, 
                                valor = valor)
                        if(saldo_atual_saque and extrato_atual_saque and numero_saques_atual_saque):
                                saldo = saldo_atual_saque
                                extrato = extrato_atual_saque
                                numero_saques = numero_saques_atual_saque
                elif(opcao == 3):
                        exibir_extrato(saldo, extrato = extrato)
                elif(opcao == 0):
                        print("Até logo.")
                        break
                else:
                        print("Opção inválida, por favor insira uma opção válida")

main()