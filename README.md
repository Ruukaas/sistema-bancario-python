# Banco Digital Python 🏦 
### Simulação de um banco digital utilizando funções de entrada e saída em Python
<div align="center"><img src="assets/Animação-v2.gif"/></div>

## Objetivo 🎯
Aplicar o conhecimento de operadores, declaração de variáveis,estruturas condicionais e de repetição, manipulação de strings,coleções, o objeto datetime e boas práticas na linguagem Python através de um sistema de banco.

## Regras de Negócio 📃
### [V1](http://academiapme-my.sharepoint.com/:p:/g/personal/kawan_dio_me/Ef-dMEJYq9BPotZQso7LUCwBJd7gDqCC2SYlUYx0ayrGNQ?e=G79e2L) 
---
### V2
- Separar as funções existentes em saque, depósito e extrato em funções
  - Função saque deve receber apenas argumentos por nome (keyword only). Sugestão: saldo, valor, extrato, limite, número saques, limite saques.
  - Função depósito deve receber os argumentos apenas por posição (positional only). Sugestão: saldo, valor, extrato. Sugestão de retorno: saldo e extrato.
  - Função extrato deve receber os argumentos por posição e nome (positional only e keyword only). Argumentos posicionais: saldo, argumentos nomeados: extratos.
- Criar duas novas funções: cadastrar usuário (cliente) e cadastrar conta bancária
  - Criar usuário (cliente): O programa deve armazenar os usuários em uma lista, um usuário é composto por: nome, data de nascimento, CPF e endereço. O endereço é uma String com o formato: logradouro - nro - bairro - cidade/sigla estado. Deve ser armazenado somente os números do CPF (sem traço e etc, e é uma String), não podemos cadastrar 2 usuários com o mesmo CPF.
  - Criar conta corrente: armazenar as contas em uma lista, a conta é composta por: agência, número da conta e usuário. O número da conta é sequencial, iniciando em 1. O número da agência é fixo: "0001". O usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário.
## Pré - Requisitos 📚
- Python 3
