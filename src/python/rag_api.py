import os
import logging
import uuid
import re
from flask import Flask, request, jsonify
from qdrant_client import QdrantClient
from langchain_core.prompts import PromptTemplate
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from langchain_gemini import llm, embed_model
from settings import settings


app = Flask(__name__)

qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    timeout=60.0
)

TEXT_DIR = "/app/extracted_texts"

# Configuração do Logger para registrar eventos e erros.
logging.basicConfig(level=settings.LOG_LEVEL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
#
# --- FIM DA CORREÇÃO ---


# Agente 2: Função para extrair o ano
def extract_year_from_query(query: str):
    """Extrai um ano de 4 dígitos da string de busca."""
    match = re.search(r'\b(20\d{2})\b', query)
    return int(match.group(1)) if match else None


# Definição do prompt e da cadeia de RAG
prompt_template = """
Você é um assistente de pesquisa altamente preciso e especializado em documentos do Ministério Público de Contas do Estado do Pará (MPC-PA). Sua tarefa é responder à pergunta do usuário baseando-se estritamente no contexto das portarias fornecidas.

**Instruções:**
1. Responda de forma clara, objetiva e em português.
2. Sintetize a informação se ela estiver contida em múltiplos trechos do contexto.
3. Ao final da sua resposta, cite o nome do arquivo da portaria usada como fonte entre colchetes. Por exemplo: [Fonte: portaria_123-2024.pdf].
4. Se a resposta exata não puder ser encontrada no contexto, responda: "Com base nos documentos fornecidos, não encontrei uma resposta direta para esta pergunta." Não tente adivinhar.

**Contexto Fornecido:**
---
{context}
---

**Pergunta do Usuário:** {question}

**Resposta Concisa:**
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
rag_chain = prompt | llm


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "Nenhuma pergunta fornecida"}), 400

    try:
        year_constraint = extract_year_from_query(question)
        query_filter = None
        limit = settings.RETRIEVAL_LIMIT

        if year_constraint:
            logger.info(f"Agente 2: Ativando filtro de metadados no Qdrant para o ano: {year_constraint}")
            query_filter = Filter(
                must=[
                    FieldCondition(key="year", match=MatchValue(value=year_constraint))
                ]
            )
            limit = settings.FILTERED_RETRIEVAL_LIMIT

        logger.info(f"Buscando até {limit} docs para: '{question}'")
        found_docs = qdrant_client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=embed_model.embed_query(question),
            query_filter=query_filter,
            limit=limit
        )

        if not found_docs:
            return jsonify({"answer": "Não encontrei nenhuma portaria relevante para responder a sua pergunta.", "sources": []})
        
        logger.info(f"Encontrados {len(found_docs)} documentos relevantes.")

        context = ""
        sources = []
        sources_seen = set()

        for doc in found_docs:
            context += f"Fonte: {doc.payload['source']}\\n"
            context += f"Título: {doc.payload['title']}\\n"
            context += f"Conteúdo do trecho: {doc.payload.get('page_content', '')}\\n\\n---\\n\\n"
            
            source_filename = doc.payload['source']
            if source_filename not in sources_seen:
                sources.append({
                    "id": os.path.splitext(source_filename)[0],
                    "title": doc.payload['title']
                })
                sources_seen.add(source_filename)

        logger.info("Gerando resposta com o LLM...")
        response = rag_chain.invoke({"context": context, "question": question})
        answer = response.content

        return jsonify({
            "answer": answer,
            "sources": sources
        })

    except Exception as e:
        logger.error(f"Erro na API RAG: {e}", exc_info=True)
        return jsonify({"error": "Ocorreu um erro ao processar sua pergunta."}), 500


@app.route('/search', methods=['POST'])
def search_documents():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({"error": "Nenhuma consulta fornecida"}), 400

    try:
        year_constraint = extract_year_from_query(query)
        query_filter = None
        limit = settings.RETRIEVAL_LIMIT

        if year_constraint:
            logger.info(f"Agente 2: Ativando filtro de metadados no Qdrant para o ano: {year_constraint}")
            query_filter = Filter(
                must=[
                    FieldCondition(key="year", match=MatchValue(value=year_constraint))
                ]
            )
            limit = settings.FILTERED_RETRIEVAL_LIMIT
        
        logger.info(f"Buscando até {limit} portarias para: '{query}'")
        found_docs = qdrant_client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=embed_model.embed_query(query),
            query_filter=query_filter,
            limit=limit
        )

        if not found_docs:
            return jsonify({"results": []})

        results = []
        for doc in found_docs:
            snippet = doc.payload.get('page_content', '')
            results.append({
                "id": os.path.splitext(doc.payload['source'])[0],
                "title": doc.payload['title'],
                "score": doc.score,
                "snippet": (snippet[:250] + '...') if len(snippet) > 250 else snippet
            })
        
        return jsonify({"results": results})

    except Exception as e:
        logger.error(f"Erro na API de busca semântica: {e}", exc_info=True)
        return jsonify({"error": "Ocorreu um erro ao processar sua busca."}), 500


@app.route('/document/<doc_id>', methods=['GET'])
def get_document(doc_id):
    try:
        sanitized_doc_id = re.sub(r'[^\w\-_\.]', '_', doc_id)
        
        filename = f"{sanitized_doc_id}.txt"
        filepath = os.path.join(TEXT_DIR, filename)

        if not os.path.exists(filepath):
            logger.error(f"Arquivo de texto NÃO ENCONTRADO em: {filepath}")
            logger.info(f"(ID original recebido do frontend: '{doc_id}')")
            return jsonify({"error": "Arquivo de texto completo não encontrado no servidor."}), 404

        with open(filepath, 'r', encoding='utf-8') as f:
            full_content = f.read()
            cleaned_content = full_content.split('Text: ', 1)[1].strip() if 'Text: ' in full_content else full_content

        response_data = {
            "_id": doc_id,
            "title": f"Conteúdo Completo: {doc_id}",
            "content": cleaned_content
        }
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Erro ao buscar documento {doc_id}: {e}", exc_info=True)
        return jsonify({"error": "Erro interno ao buscar o documento."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)