# Aplicação de Busca Inteligente de Portarias (RAG)

## Visão Geral

Esta aplicação implementa um sistema de **Busca Aumentada por Geração (RAG - Retrieval-Augmented Generation)** para consultar "portarias" (documentos administrativos oficiais) do "Ministério Público de Contas do Estado do Pará" (MPC-PA). O sistema automatiza o download dos PDFs do portal de transparência, extrai seu conteúdo, o indexa em um banco de dados vetorial e permite que os usuários façam perguntas em linguagem natural ou realizem buscas semânticas sobre os documentos.

## Arquitetura do Sistema

A aplicação é composta pelos seguintes componentes principais, orquestrados via Docker Compose:

1.  **Frontend (Vue.js + Quasar):** Interface web reativa que oferece duas funcionalidades principais: um chat para fazer perguntas sobre os documentos e uma tela de busca semântica para encontrar portarias por assunto.
2.  **RAG API (Flask + LangChain):** O cérebro do sistema. Esta API recebe as perguntas do usuário, busca por informações relevantes no banco de dados vetorial e utiliza um Grande Modelo de Linguagem (LLM), como o Google Gemini, para formular uma resposta precisa baseada nos documentos encontrados.
3.  **Ingestor de Dados (`python-updater`):** Um serviço em Python responsável por todo o pipeline de ETL: baixar os PDFs, processá-los (com OCR quando necessário), extrair metadados (como título e ano), gerar os vetores (embeddings) e carregar os dados no Qdrant.
4.  **Qdrant:** Um banco de dados vetorial de alta performance, utilizado para armazenar os "embeddings" dos documentos e permitir buscas de similaridade em alta velocidade.
5.  **Nginx:** Servidor web que serve a aplicação frontend e atua como um proxy reverso para a RAG API, centralizando o acesso.

## Pré-requisitos

* **Docker:** Essencial para containerizar e executar a aplicação.
* **Docker Compose:** Utilizado para definir e gerenciar a aplicação multi-container.

## Configuração e Instalação

1.  **Clone o Repositório:**
    ```bash
    git clone <url_do_repositorio>
    cd <diretorio_do_repositorio>
    ```

2.  **Configuração de Ambiente:**
    * Crie um arquivo `.env` na raiz do projeto a partir do exemplo abaixo.
    * Insira sua chave da API do Google no campo `GOOGLE_API_KEY`.

        ```
        # Porta para o frontend
        PORT=3000
        
        # Chave da API do Google para os modelos Gemini
        GOOGLE_API_KEY="SUA_CHAVE_API_AQUI"
        ```

3.  **Inicie a Aplicação:**
    * Use o Docker Compose para construir as imagens e iniciar os containers:
    ```bash
    docker-compose up --build -d
    ```
    Este comando iniciará todos os serviços em modo `detached`. O serviço `python-updater` será executado uma vez para popular o banco de dados e depois será finalizado.

## Acessando a Aplicação

Após a inicialização, a aplicação estará acessível no seu navegador em: http://localhost:3000

(Pode levar alguns minutos para o primeiro processamento de dados ser concluído).

## Atualizando a Base de Dados

Para buscar novas portarias e atualizar o banco de dados vetorial, basta executar o serviço `python-updater` novamente:

```bash
docker-compose run --rm python-updater