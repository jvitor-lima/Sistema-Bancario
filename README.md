# Sistema Bancário em FastAPI

Este é um sistema bancário básico usando FastAPI e SQLite.

## Instalação

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/jvitor-lima/Sistema-Bancario
    ```

2. **Crie e ative um ambiente virtual:**

    ```bash
    python -m venv venv

    ```

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Inicialize o banco de dados:**

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

- `POST /usuarios`: Criar um usuário
- `POST /contas`: Criar uma conta
- `GET /contas/{numero}`: Obter detalhes da conta
- `POST /contas/{numero}/depositar`: Depositar em uma conta
- `POST /contas/{numero}/sacar`: Sacar de uma conta
- `POST /contas/transferir`: Transferir entre contas
- `PUT /usuarios/{email}`: Atualizar um usuário
- `PUT /contas/{numero}`: Atualizar uma conta
- `DELETE /usuarios/{email}`: Deletar um usuário
- `DELETE /contas/{numero}`: Deletar uma conta
- `GET /usuarios`: Listar todos os usuários
- `GET /contas`: Listar todas as contas
