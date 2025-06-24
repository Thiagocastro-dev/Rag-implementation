import os
import logging
import uuid
import re  # Garanta que esta linha de import exista no topo do arquivo
from flask import Flask, request, jsonify
from qdrant_client import QdrantClient
from langchain_core.prompts import PromptTemplate

from langchain_gemini import llm, embed_model
from settings import settings

app = Flask(__name__)
qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    timeout=60.0
)

TEXT_DIR = "/app/extracted_texts"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# (O prompt_template e o rag_chain permanecem os mesmos)
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
        logger.info(f"Buscando documentos para a pergunta: '{question}'")
        found_docs = qdrant_client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=embed_model.embed_query(question),
            limit=7
        )
        
        if not found_docs:
            return jsonify({"answer": "Não encontrei nenhuma portaria relevante para responder a sua pergunta.", "sources": []})

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


# --- FUNÇÃO CORRIGIDA ---
@app.route('/document/<doc_id>', methods=['GET'])
def get_document(doc_id):
    """
    Busca e retorna o CONTEÚDO COMPLETO de um documento
    baseado no seu ID (que é o nome do arquivo sem extensão).
    """
    try:
        # Sanitiza o ID recebido para corresponder ao nome do arquivo no disco
        sanitized_doc_id = re.sub(r'[^\w\-_\.]', '_', doc_id)
        
        # Usa o ID sanitizado para montar o caminho do arquivo
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