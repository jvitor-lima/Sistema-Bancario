# Sistema Bancário

Este é um sistema bancário simples, desenvolvido em Python, que permite criar usuários e contas, realizar depósitos, saques, transferências e verificar o saldo e o histórico de transações. Os dados dos usuários e das contas são armazenados localmente em arquivos JSON.

## Funcionalidades

- Criação de usuários e contas bancárias.
- Autenticação de usuários.
- Depósitos, saques e transferências entre contas.
- Visualização de saldo e histórico de transações.
- Persistência de dados em arquivos JSON.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

- `app.py`: Este arquivo é o ponto de entrada do aplicativo FastAPI.
- `conta.py`: Define a classe `Conta` e suas funcionalidades.
- `main.py`: Arquivo principal que contém o menu de interação com o usuário e a lógica de carregamento e salvamento de dados.
- `README.md`: Este arquivo
- `requirements.txt`:  Arquivo com as dependências o fastapi e o uvicorn
- `test_sistema.py`: Arquivo de testes automatizados para verificar o funcionamento do sistema.
- `usuario.py`: Define a classe `Usuario` e suas funcionalidades.

## Como Executar

1. Clone o repositório para sua máquina local.
2. Certifique-se de ter o Python instalado.
3. Navegue até o diretório do projeto no terminal.
4. Execute o script `main.py` para iniciar o sistema bancário:

## Testes

Para executar os testes automatizados, execute o seguinte comando no terminal:
`python test_sistema.py`

## Dependencias

Este projeto possui dependencias fastapi e uvicorn

## Contribuintes

- Vitor Lima

- Rodrigo Santos

## Licença

Este projeto está licenciado sob a MIT License.

## Contatos

Para mais informações, entre em contato com os contribuindores:

- Vitor Lima: josevitoroff@gmail.com

- Rodrigo Santos: rds.beserra@gmail.com
