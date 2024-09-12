from abc import ABC, abstractmethod #@abstractclassmethod e @abstractproperty deprecated since 3.3
from datetime import datetime, date
from __future__ import annotations #Forward references para utilizar type hints, a partir do Python 3.7
class Conta():
        def __init__(self, numeroConta: int, cliente: Cliente):
                self._saldo = 0
                self._numeroConta = numeroConta
                self._agencia = "0001"
                self._cliente = cliente
                self._historico = Historico()
        
        @property
        def saldo(self):
                return self._saldo
        
        @property
        def numeroConta(self):
                return self._numeroConta
        
        @property
        def agencia(self):
                return self._agencia
        
        @property
        def cliente(self):
                return self._cliente
        
        @property
        def historico(self):
                return self._historico
                
        @classmethod
        def nova_conta(cls,numeroConta: int, cliente: Cliente):
                return cls(numeroConta, cliente)
        
        def sacar(self,valor: float):
                saldo = self.saldo
                excedeu_saldo = valor > saldo
                saque_concluido_com_sucesso = False
        
                if(excedeu_saldo):
                        print("Operação não realizada. Valor maior que saldo disponível")
                elif(valor > 0): 
                        self._saldo -= valor
                        saque_concluido_com_sucesso = True
                        print(f"Saque no valor de R$ {valor:.2f} realizado com sucesso\n")
                else:
                        print("Operação não realizada. Insira um valor válido\n")
                        
                return saque_concluido_com_sucesso
        
        def depositar(self,valor: float):
                deposito_concluido_com_sucesso = False
                if(valor > 0):
                        self._saldo += valor
                        deposito_concluido_com_sucesso = True    
                        print(f"Depósito no valor de R$ {valor:.2f} realizado com sucesso\n")
                else:
                        print("Operação não realizada. O valor informado é inválido.\n")
                
                return deposito_concluido_com_sucesso
                
class Transacao(ABC):
        @property
        @abstractmethod
        def valor(self):
                pass
        
        @classmethod
        @abstractmethod
        def registrar(self, conta: Conta):
                pass

class Cliente():
        def __init__(self, endereco: str):
                self.endereco = endereco
                self.contas = []
                
        def realizar_transacao(self,conta: Conta , transacao: Transacao):
                transacao.registrar(conta)
        
        def adicionar_conta(self, conta : Conta):
                self.contas.append(conta)

class PessoaFisica(Cliente):
        def __init__(self, nome: str, data_nascimento: date, cpf: str, endereco: str):
                super().__init__(endereco)
                self.nome = nome
                self.data_nascimento = data_nascimento
                self.cpf = cpf

class Saque(Transacao):
        def __init__(self, valor: float):
                self._valor = valor

        @property
        def valor(self):
                return self._valor

        def registrar(self, conta: Conta):
                sucesso_transacao = conta.sacar(self.valor)

                if sucesso_transacao:
                        conta.historico.adicionar_transacao(self)
class Deposito(Transacao):
        def __init__(self, valor: float):
                self._valor = valor

        @property
        def valor(self):
                return self._valor

        def registrar(self, conta: Conta):
                sucesso_transacao = conta.depositar(self.valor)

                if sucesso_transacao:
                        conta.historico.adicionar_transacao(self)
                        
class Historico():
        def __init__(self):
                self._transacoes = []
        
        @property
        def transacoes(self):
                return self._transacoes
        
        def adicionar_transacao(self, transacao: Transacao):
                self._transacoes.append(
                        {
                                "Tipo de Transação": transacao.__class__.__name__,
                                "Valor": transacao.valor,
                                "Data/Hora": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
                        }
                )

class ContaCorrente(Conta):
        def __init__(self, numeroConta: int, cliente: Cliente, limite: int=500 , limite_saques: int=3):
                super().__init__(numeroConta, cliente)
                self.limite = limite
                self.limite_saques = limite_saques
        
        def sacar(self, valor:float):
                numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["Tipo de Transação"] == Saque.__name__])
                excedeu_limite_saques = numero_saques >= self.limite_saques
                excedeu_limite_valor_saque = valor > self.limite
                saque_concluido_com_sucesso = False
                
                if(excedeu_limite_saques): 
                        print("Operação não realizada. Limite de saques atingido.\n") 
                elif(excedeu_limite_valor_saque): 
                        ("Operação não realizada. Limite de valor de saque atingido.\n") 
                else:
                        super().sacar(valor)
                
                return saque_concluido_com_sucesso


def menu():
        menu = """Escolha a operação desejada:
[1] Depositar
[2] Sacar
[3] Extrato
[4] Cadastrar novo usuário
[5] Criar uma nova conta
[6] Listar contas cadastradas
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

def exibir_contas(contas):
        if(len(contas) == 0):
                print("Não foram criadas nenhuma conta")
        else:
                print("########## - Contas - ###############")
                for indice, entrada in enumerate(contas):
                        print(f"Conta {indice+1}: {entrada}")
                print("######################################")
                print()
          
def filtrar_usuario(cpf, usuarios):
        usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

def validar_cpf(cpf):
    if(len(cpf) == 11 and cpf.isdigit()):
        return True
    else:
        return False

def validar_data_formato_br(data):
        try:
                datetime.strptime(data, '%d-%m-%Y')
                return True
        except ValueError:
                return False
        
def validar_endereço(endereço):
        try:
                rua, resto = endereço.split(',', 1) 
                numero, resto = resto.split(' - ', 1)
                bairro, resto = resto.split(' - ', 1)
                cidade, estado = resto.split('/', 1)
        
                if (rua.strip() and numero.strip().isdigit() and bairro.strip() and cidade.strip() and len(estado.strip()) == 2 and estado.isupper()):
                        return True
                else:
                        return False
        except ValueError:
                return False
        
def criar_entrada_usuario(cpf):
        nome = input("Informe o nome completo: ")
        
        data_nascimento = input("Informe a data de nascimento (Exatamente no seguinte formato: dd-mm-aaaa): ")
        data_valida = validar_data_formato_br(data_nascimento)
        if(not data_valida):
                print("Operação não realizada. Data inserida em um formato errado")
                return
        
        endereco = input("Informe o endereço (Exatamente no seguinte formato: logradouro, numero - bairro - cidade/sigla estado): ")
        endereco_valido = validar_endereço(endereco)
        if(not endereco_valido):
                print("Operação não realizada. Endereço inserido em um formato errado.")
                return
                
        return {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}

def criar_usuario(usuarios):
        cpf = input("Informe o CPF para o cadastro(somente números, 11 digitos): ")
        cpf_valido = validar_cpf(cpf)
        if(not cpf_valido):
                print("Operação não realizada. CPF inválido")
                return
        
        usuario = filtrar_usuario(cpf, usuarios)
        
        if(usuario): #Se já existir um usuário com esse CPF cadastrado
                print("Operação não realizada. CPF já cadastrado.")
                return 
        
        usuario = criar_entrada_usuario(cpf)
        if(usuario): #Se ele conseguiu criar o usuário com sucesso
                usuarios.append(usuario)
                print(f"Usuário {usuario["nome"]} com o CPF {cpf} foi criado com sucesso.\n")
                
def criar_conta(agencia, numero_conta, usuarios,contas):
        conta_criada_com_sucesso = False
        cpf = input("Informe o CPF(somente números, 11 digitos): ")
        cpf_valido = validar_cpf(cpf)
        if(not cpf_valido):
                print("Operação não realizada. CPF inválido")
                return
        
        usuario = filtrar_usuario(cpf, usuarios)
        if(usuario): #Se existir um usuário com esse CPF cadastrado para que possamos cadastrar a conta
                conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
                contas.append(conta)
                print(f"Conta {numero_conta} na Agência {agencia} criada com sucesso.")
                conta_criada_com_sucesso = True
        else:
                print("Operação não realizada. Nenhum usuário encontrado com esse CPF")
        
        return conta_criada_com_sucesso
                
def main():
        boas_vindas = "Bem vindo ao seu sistema bancário!"
        
        saldo = 0
        limite = 500
        extrato = []
        numero_saques = 0
        LIMITE_SAQUES = 3
        usuarios = []
        contas = []
        numero_conta_sequencial = 1 #Começa com 1 e vai incrementando
        AGENCIA = "0001"
        
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
                elif(opcao == 4):
                        criar_usuario(usuarios)
                elif(opcao == 5):
                        conta_criada_com_sucesso = criar_conta(AGENCIA, numero_conta_sequencial, usuarios,contas)
                        if(conta_criada_com_sucesso):
                                numero_conta_sequencial+=1
                elif(opcao == 6):
                        exibir_contas(contas)
                elif(opcao == 0):
                        print("Até logo.")
                        break
                else:
                        print("Opção inválida, por favor insira uma opção válida")

main()