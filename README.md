# Sistema Bancário em FastAPI

Este é um sistema bancário básico usando FastAPI e SQLite.

## Instalação

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/jvitor-lima/Sistema-Bancario
    ```


2. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Inicialize o banco de dados:**

    ```bash
    python -c "import database; database.inicializar_bd()"
    ```

## Uso

1. **Inicie o servidor:**

    ```bash
    uvicorn app:app --reload
    ```

2. **Acesse a API em:** [http://localhost:8000](http://localhost:8000)


## Endpoints

### Usuários

- `POST /usuarios`: Criar um usuário.
- `PUT /usuarios/{email}`: Atualizar os dados de um usuário existente.
- `DELETE /usuarios/{email}`: Deletar um usuário.
- `GET /usuarios`: Listar todos os usuários.

### Contas Bancárias

- `POST /contas`: Criar uma nova conta bancária.
- `GET /contas/{numero}`: Obter os detalhes de uma conta específica.
- `PUT /contas/{numero}`: Atualizar os dados de uma conta bancária.
- `DELETE /contas/{numero}`: Deletar uma conta bancária.
- `POST /contas/{numero}/depositar`: Realizar um depósito em uma conta.
- `POST /contas/{numero}/sacar`: Realizar um saque de uma conta.
- `POST /contas/transferir`: Realizar transferência entre contas.
- `GET /contas`: Listar todas as contas bancárias.