from __future__ import annotations #Forward references para utilizar type hints, a partir do Python 3.7
from abc import ABC, abstractmethod #@abstractclassmethod e @abstractproperty deprecated since 3.3
from datetime import datetime, date
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
                                "Data/Hora": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
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
                        print("Operação não realizada. Limite de valor de saque atingido.\n") 
                else:
                        saque_concluido_com_sucesso = super().sacar(valor)
                
                return saque_concluido_com_sucesso
        
        def __str__(self):
                return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numeroConta}
            Titular:\t{self.cliente.nome}
                """


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

def validacao_transacao_deposito_saque(usuarios:list):
        validacao_transacao_deposito_saque = False
        
        cpf = input("Informe o CPF do cliente: ")
        cpf_valido = validar_cpf(cpf)
        if(not cpf_valido):
                print("Operação não realizada. CPF inválido.\n")
                return validacao_transacao_deposito_saque, None, None
        
        usuario = filtrar_usuario(cpf, usuarios)
        if(not usuario):
                print(f"Usuário com o CPF {cpf} não encontrado.\n")
                return validacao_transacao_deposito_saque, None, None
        
        numeroConta = int(input("Informe o número da conta: "))
        conta = filtrar_conta_cliente(usuario, numeroConta)
        if(not conta):
                print(f"Conta {numeroConta} do usuário {cpf} não encontrada.\n")
                return validacao_transacao_deposito_saque, None, None
        
        validacao_transacao_deposito_saque = True
        return validacao_transacao_deposito_saque, conta, usuario
        
def depositar(usuarios: list):
        bool_validacao_transacao_deposito_saque, conta, usuario = validacao_transacao_deposito_saque(usuarios)
        if(bool_validacao_transacao_deposito_saque):
                valor = float(input("Informe o valor do depósito: "))
                transacao = Deposito(valor)
                usuario.realizar_transacao(conta, transacao)

def sacar(usuarios: list):
        bool_validacao_transacao_deposito_saque, conta, usuario = validacao_transacao_deposito_saque(usuarios)
        if(bool_validacao_transacao_deposito_saque):
                valor = float(input("Informe o valor do saque: "))
                transacao = Saque(valor)
                usuario.realizar_transacao(conta, transacao)
        
def exibir_extrato(usuarios: list):
        cpf = input("Informe o CPF do cliente: ")
        cpf_valido = validar_cpf(cpf)
        if(not cpf_valido):
                print("Operação não realizada. CPF inválido.\n")
                return
               
        usuario = filtrar_usuario(cpf, usuarios)
        if(not usuario):
                print(f"Usuário com o CPF {cpf} não encontrado.\n")
                return
        
        numeroConta = int(input("Informe o número da conta: "))
        conta = filtrar_conta_cliente(usuario, numeroConta)
        if(not conta):
                print(f"Conta {numeroConta} do usuário {cpf} não encontrada.\n")
                return
        
        print("########## - Extrato - ###############")
        transacoes = conta.historico.transacoes
        extrato = ""
        if(not transacoes):
                extrato = "Não foram realizadas movimentações.\n"
        else:
                for transacao in transacoes:
                        extrato += f"\n{transacao['Tipo de Transação']}:\n\tR$ {transacao['Valor']:.2f}"

        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("######################################")

def exibir_contas(usuarios):
        cpf = input("Informe o CPF do cliente: ")
        cpf_valido = validar_cpf(cpf)
        if(not cpf_valido):
                print("Operação não realizada. CPF inválido.\n")
                return 
        usuario = filtrar_usuario(cpf, usuarios)
        if(not usuario):
                print(f"Usuário com o CPF {cpf} não encontrado.\n")
                return
        else:
                contas = usuario.contas
                print("########## - Contas - ###############")
                if(not contas):
                        print("Não foram criadas nenhuma conta.\n")
                for conta in contas:
                        print(str(conta))
                print("######################################")
                print()
          
def filtrar_usuario(cpf: str, usuarios: list):
        usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

def filtrar_conta_cliente(usuario: Cliente, numeroConta: int):
        if(not usuario.contas):
                return
        else:
                contas_usuario = [conta for conta in usuario.contas if conta.numeroConta == numeroConta]
                return contas_usuario[0] if contas_usuario else None

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
                print("Operação não realizada. Data inserida em um formato errado.\n")
                return
        data_nascimento = datetime.strptime(data_nascimento,'%d-%m-%Y')
        
        endereco = input("Informe o endereço (Exatamente no seguinte formato: logradouro, numero - bairro - cidade/sigla estado): ")
        endereco_valido = validar_endereço(endereco)
        if(not endereco_valido):
                print("Operação não realizada. Endereço inserido em um formato errado.\n")
                return
                
        return {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}

def criar_usuario(usuarios):
        cpf = input("Informe o CPF para o cadastro(somente números, 11 digitos): ")
        cpf_valido = validar_cpf(cpf)
        if(not cpf_valido):
                print("Operação não realizada. CPF inválido\n")
                return 
        
        usuario = filtrar_usuario(cpf, usuarios)
        
        if(usuario): #Se já existir um usuário com esse CPF cadastrado
                print("Operação não realizada. CPF já cadastrado.\n")
                return 
        
        usuario_dados = criar_entrada_usuario(cpf)
        if(usuario_dados): #Se ele conseguiu criar os dados do usuário com sucesso
                usuario = PessoaFisica(usuario_dados["nome"],usuario_dados["data_nascimento"],usuario_dados["cpf"],usuario_dados["endereco"])
                usuarios.append(usuario)
                print(f"Usuário {usuario.nome} com o CPF {cpf} foi criado com sucesso.\n")
                
def criar_conta(numero_conta, usuarios):
        conta_criada_com_sucesso = False
        cpf = input("Informe o CPF(somente números, 11 digitos): ")
        cpf_valido = validar_cpf(cpf)
        if(not cpf_valido):
                print("Operação não realizada. CPF inválido")
                return conta_criada_com_sucesso
        
        usuario = filtrar_usuario(cpf, usuarios)
        if(usuario): #Se existir um usuário com esse CPF cadastrado para que possamos cadastrar a conta
                conta = ContaCorrente(numero_conta,usuario)
                usuario.contas.append(conta)
                print(f"Conta {numero_conta} do usuário {usuario.nome} criada com sucesso.")
                conta_criada_com_sucesso = True
        else:
                print("Operação não realizada. Nenhum usuário encontrado com esse CPF")
        
        return conta_criada_com_sucesso
                
def main():
        boas_vindas = "Bem vindo ao seu sistema bancário!"
       
        usuarios = []
        numero_conta_sequencial = 1
        print(boas_vindas)
        
        while(True):
                opcao = menu()

                if(opcao == 1):
                        depositar(usuarios)
                elif(opcao == 2):
                        sacar(usuarios)
                elif(opcao == 3):
                        exibir_extrato(usuarios)
                elif(opcao == 4):
                        criar_usuario(usuarios)
                elif(opcao == 5):
                        conta_criada_com_sucesso = criar_conta(numero_conta_sequencial, usuarios)
                        if(conta_criada_com_sucesso):
                                numero_conta_sequencial+=1
                elif(opcao == 6):
                        exibir_contas(usuarios)
                elif(opcao == 0):
                        print("Até logo.")
                        break
                else:
                        print("Opção inválida, por favor insira uma opção válida")

main()