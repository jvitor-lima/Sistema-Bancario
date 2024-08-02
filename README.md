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

## Executando API
Para rodar a API,execute o comando abaixo no terminal
`uvicorn app:app --reload`
A API estará disponível no endereço `http://127.0.0.1:8000`.

## Requisições de teste
Você pode testar os endpoints da API usando o `curl`
comando pra criar usuário: `curl -X POST -H "Content-Type: application/json" -d '{"nome": "Vitor", "email": "Vitor@gmail.com", "senha": "senha1234"}' http://127.0.0.1:8000/usuarios`
comando para criar conta: `curl -X POST -H "Content-Type: application/json" -d '{"email": "Vitor@gmail.com", "saldo_inicial": 1000.0}' http://127.0.0.1:8000/contas`
comando para obter detalhes de uma conta: `curl -X GET http://127.0.0.1:8000/contas/10`
comando para depositar: `curl -X POST -H "Content-Type: application/json" -d '{"valor": 500.0}' http://127.0.0.1:8000/contas/10/depositar`
comando para sacar: `curl -X POST -H "Content-Type: application/json" -d '{"valor": 200.0}' http://127.0.0.1:8000/contas/10/sacar`
comando para transferir: `curl -X POST -H "Content-Type: application/json" -d '{"conta_origem": 10, "conta_destino": 20, "valor": 100.0}' http://127.0.0.1:8000/contas/transferir`

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
