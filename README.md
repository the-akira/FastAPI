# Experimento FastAPI

Aplicação construída com FastAPI e SQLModel, utilizando Docker para facilitar o setup do ambiente. Ela permite fazer scraping de conteúdo da web e armazenar os dados em um banco de dados PostgreSQL. Também possibilita o envio de e-mails de forma assíncrona em segundo plano.

## Requisitos

- Docker
- Docker Compose

## Instalação

### Clonar o Repositório

```
git clone https://github.com/the-akira/FastAPI.git
cd FastAPI
```

### Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
EMAIL=enderecoemail
EMAIL_PASSWORD=senhaemail
```

Substitua as informações com as suas credenciais.

### Construir e Subir os Containers

```
docker-compose up --build
```

Isso vai construir os containers e iniciar a aplicação.

### Executando Migrações com Alembic

```
docker-compose exec web alembic revision --autogenerate -m "Initial migration"
docker-compose exec web alembic upgrade head
```

### Uso

A aplicação estará disponível em `http://127.0.0.1:8000`.

### Documentação

Você pode acessar a documentação automática da API em `http://127.0.0.1:8000/docs`.