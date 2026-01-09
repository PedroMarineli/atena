# Atena

Sistema de gestão empresarial (ERP) simplificado, desenvolvido para auxiliar pequenas empresas no controle de estoque, vendas e financeiro.

## 🚀 Tecnologias Utilizadas

- **Backend:** [Django 5.1](https://www.djangoproject.com/) (Python)
- **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/)
- **Frontend:**
  - [Tailwind CSS](https://tailwindcss.com/) (Estilização)
  - [Alpine.js](https://alpinejs.dev/) (Interatividade leve)
  - [HTMX](https://htmx.org/) (Requisições dinâmicas sem Page Reload)
- **Infraestrutura:** [Docker](https://www.docker.com/) & Docker Compose

## 📋 Funcionalidades

O sistema é dividido em módulos principais:

- **Dashboard:** Visão geral do negócio com acesso rápido aos módulos.
- **Inventário (`inventory`):**
  - Cadastro de Produtos e Serviços
  - Categorização de itens
  - Gestão de Fornecedores
  - Controle de Estoque (com alertas de estoque mínimo)
- **Vendas (`sales`):**
  - Gestão de Clientes
  - Realização de Vendas (Produtos e Serviços)
  - Status de pedidos (Pendente, Finalizada, Cancelada)
- **Financeiro (`finance`):**
  - Controle de Receitas e Despesas
  - Contas a Pagar e Receber
- **Administração:** Gestão de usuários e configurações da organização.

## 🛠️ Pré-requisitos

Para rodar o projeto, você precisa ter instalado:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## ⚙️ Configuração e Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/atena.git
   cd atena
   ```

2. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto baseando-se no exemplo:
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` com suas configurações (ex: credenciais do banco).

3. **Suba os containers com Docker Compose:**
   ```bash
   docker-compose up -d --build
   ```

4. **Acesse a aplicação:**
   O sistema estará disponível em: [http://localhost:8888](http://localhost:8888)

## 🐳 Comandos Úteis

- **Criar superusuário (Admin):**
  ```bash
  docker-compose exec atena-django python manage.py createsuperuser
  ```

- **Rodar migrações manualmente (se necessário):**
  ```bash
  docker-compose exec atena-django python manage.py migrate
  ```

- **Ver logs da aplicação:**
  ```bash
  docker-compose logs -f atena-django
  ```

## 🧪 Estrutura do Projeto

- `core/`: Configurações principais do Django.
- `dashboard/`: Lógica da página inicial e templates comuns.
- `inventory/`: Modelos e views de produtos e estoque.
- `sales/`: Lógica de vendas e clientes.
- `finance/`: Controle financeiro.
- `templates/`: Templates HTML globais e parciais.
- `docker-compose.yml`: Orquestração dos containers.
