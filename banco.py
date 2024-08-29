menu = """Escolha a operação desejada:
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
-->"""

boas_vindas = "Bem vindo ao seu sistema bancário!"

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

print(boas_vindas)
while(True):
        opcao = int(input(menu))
        if(opcao == 1):
                print("Depósito")
        elif(opcao == 2):
                print("Sacar")
        elif(opcao == 3):
                print("Extrato")
        elif(opcao == 0):
                print("Até logo.")
                break
        else:
                print("Opção inválida, por favor insira uma opção válida")
