import os
import logging
from langchain_core.documents import Document
from qdrant_client import QdrantClient, models

from pdf_downloader import download_pdfs_first_page
from pdf_processor import process_single_pdf
from langchain_gemini import embed_model
from settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestPortarias:
    def __init__(self, pdf_dir="/app/pdfs", text_dir="/app/extracted_texts"):
        self.pdf_dir = pdf_dir
        self.text_dir = text_dir
        self.qdrant_client = QdrantClient(url=settings.QDRANT_URL)
        self.collection_name = settings.QDRANT_COLLECTION
        
        os.makedirs(self.pdf_dir, exist_ok=True)
        os.makedirs(self.text_dir, exist_ok=True)

    def _setup_qdrant_collection(self):
        try:
            self.qdrant_client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=768,
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Coleção '{self.collection_name}' recriada no Qdrant.")
        except Exception as e:
            logger.warning(f"Não foi possível recriar a coleção (pode já existir): {e}")

    def run_ingestion(self):
        logger.info("Iniciando o processo de ingestão de portarias.")
        
        logger.info("Baixando PDFs do portal...")
        download_pdfs_first_page(
            url=settings.MPC_PORTARIAS_URL,
            output_dir=self.pdf_dir
        )
        
        pdf_files = [f for f in os.listdir(self.pdf_dir) if f.endswith('.pdf')]
        if not pdf_files:
            logger.warning("Nenhum PDF novo encontrado. Finalizando a ingestão.")
            return

        self._setup_qdrant_collection()

        all_documents = []
        for filename in pdf_files:
            pdf_path = os.path.join(self.pdf_dir, filename)
            logger.info(f"Processando: {filename}")
            
            result = process_single_pdf(pdf_path, self.text_dir)
            
            if result and result.get('title') != 'Error':
                text_file_path = os.path.join(self.text_dir, os.path.splitext(filename)[0] + '.txt')
                if os.path.exists(text_file_path):
                    with open(text_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        text_content = content.split('Text: ', 1)[1].strip() if 'Text: ' in content else content

                    doc = Document(
                        page_content=text_content,
                        metadata={
                            "source": filename,
                            "title": result.get('title', 'Sem título')
                        }
                    )
                    all_documents.append(doc)

        if not all_documents:
            logger.warning("Nenhum documento válido para vetorizar.")
            return

        # --- INÍCIO DA CORREÇÃO DE PROCESSAMENTO EM LOTES ---
        batch_size = 100  # Processa 100 documentos por vez
        total_docs = len(all_documents)
        logger.info(f"Iniciando vetorização e upload de {total_docs} documentos em lotes de {batch_size}.")

        for i in range(0, total_docs, batch_size):
            batch = all_documents[i:i + batch_size]
            logger.info(f"Processando lote {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size} (documentos {i+1} a {i+len(batch)})")

            contents_to_embed = [doc.page_content for doc in batch]
            doc_ids = [os.path.splitext(doc.metadata['source'])[0] for doc in batch]

            try:
                embeddings = embed_model.embed_documents(contents_to_embed)
                
                self.qdrant_client.add(
                    collection_name=self.collection_name,
                    documents=contents_to_embed,
                    embeddings=embeddings,
                    metadatas=[doc.metadata for doc in batch],
                    ids=doc_ids
                )
            except Exception as e:
                logger.error(f"Erro ao processar o lote de documentos {i+1}-{i+len(batch)}: {e}")
                # Decide se quer parar ou continuar com o próximo lote
                # Por agora, vamos continuar
                continue
        # --- FIM DA CORREÇÃO ---
        
        logger.info("Processo de ingestão concluído com sucesso.")