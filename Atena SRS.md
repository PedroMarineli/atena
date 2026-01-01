# **Especificação de Requisitos de Software (SRS)**

**Projeto:** Atena   
**Versão:** 1.0  
**Data:** 01/12/2025  
**Autor:** Pedro Henrique Marineli de Oliveira

## **1\. Introdução**

### **1.1. Propósito**

O propósito deste documento é detalhar os requisitos para o desenvolvimento do **Atena**, um sistema de gestão simplificado para Pequenas e Médias Empresas (PMEs). O objetivo principal é centralizar vendas, estoque e financeiro, demonstrando competências técnicas em arquitetura de software e regras de negócio para fins de portfólio.

### **1.2. Público-Alvo**

* **Equipe de Desenvolvimento:** Guia para implementação.  
* **Recrutadores e Avaliadores:** Demonstração de capacidade de análise.  
* **Designers UI/UX:** Base para prototipagem.

### **1.3. Escopo do Produto**

###    **O que o sistema FAZ:**

* Gestão de Acesso (Login e Permissões).  
* Cadastro de Clientes, Fornecedores e Produtos.  
* Controle de Estoque (Entradas e Saídas).  
* Ponto de Venda (PDV) para geração de pedidos.  
* Gestão Financeira (Contas a Pagar/Receber e Fluxo de Caixa).  
* Dashboard com indicadores (KPIs).

    **O que o sistema NÃO FAZ (Versão 1.0):**

* Emissão real de NFe (integração governamental).  
* Módulo de RH/Folha de Pagamento.  
* Integração com E-commerce.  
* App Mobile Nativo.

## **2\. Descrição Geral**

### **2.1. Restrições Tecnológicas**

| Componente | Tecnologia Sugerida |
| :---- | :---- |
| **Backend e Frontend** | Django + alpine e htmx|
| **Banco de Dados** | PostgreSQL |
| **Infraestrutura** | Local |

### **2.2. Suposições e Dependências**

* Conexão estável com a internet (Modelo SaaS Web).  
* Uso de bibliotecas de terceiros para gráficos (ex: Chart.js).  
* Uso de API externa para consulta de CEP (ex: ViaCEP).

## **3\. Requisitos Específicos**

### **3.1. Requisitos Funcionais**

#### **Módulo 01: Autenticação e Configuração**

* **\[RF-001\] Login e Autenticação**  
  * *Descrição:* Acesso via e-mail e senha.  
  * *Critério:* Implementação de Token JWT. Rotas privadas devem exigir token válido.  
* **\[RF-002\] Controle de Permissões (RBAC)**  
  * *Descrição:* Perfis de "Administrador" e "Vendedor".  
  * *Critério:* O perfil "Vendedor" não deve visualizar o menu "Financeiro".

#### **Módulo 02: Cadastros e Estoque**

* #### **\[RF-003\] Cadastro de Itens (Produtos e Serviços)** 

  * Se Tipo for "Produto": Exigir SKU e controlar Estoque.  
  * Se Tipo for "Serviço": SKU opcional e ocultar campo de Estoque.  
* **\[RF-004\] Movimentação de Estoque Inteligente**   
  * O sistema deve impedir vendas se o saldo for insuficiente APENAS se o item for do tipo "Produto".  
  * Itens do tipo "Serviço" podem ser vendidos ilimitadamente (saldo infinito ou ignorado).

#### **Módulo 03: Vendas (PDV)**

* **\[RF-005\] Realizar Pedido**  
  * *Descrição:* Interface de PDV para selecionar clientes e produtos.  
  * *Critério:* Ao finalizar, o sistema deve gerar um registro em "Contas a Receber" e debitar do estoque.

#### **Módulo 04: Financeiro**

* **\[RF-006\] Contas a Pagar e Receber**  
  * *Descrição:* Gestão de lançamentos financeiros.  
  * *Critério:* Filtros por Data, Status (Pendente/Pago) e Tipo.  
* **\[RF-007\] Fluxo de Caixa (Dashboard)**  
  * *Descrição:* Visão consolidada financeira.  
  * *Critério:* Gráfico em tempo real comparando Entradas vs. Saídas.


### **3.2. Interface e Sistema**

* **\[UI-001\] Responsividade:** Layout fluido para adaptação em Desktops e Tablets.  
* **\[API-001\] Padrão REST:** Uso correto de verbos HTTP e Status Codes.  
* **\[RS-001\] Busca Global:** Barra de pesquisa rápida (Header) para Clientes e Produtos.  
* **\[RS-002\] Exportação:** Geração de comprovante de venda simples em PDF.

### **3.3. Requisitos Não Funcionais (Qualidade)**

* **\[RNF-001\] Segurança:** Senhas criptografadas (Bcrypt/Argon2).  
* **\[RNF-002\] Performance:** Carregamento de telas críticas abaixo de 2 segundos.  
* **\[RNF-003\] Código:** Arquitetura limpa (Clean Code/SOLID).  
* **\[RNF-004\] Documentação:** API documentada via Swagger/OpenAPI.

## **4\. Apêndice**

1. **Diagrama ER (Banco de Dados)**  
2. **Protótipo de Telas (Figma)**  
3. **Collection do Yaak**