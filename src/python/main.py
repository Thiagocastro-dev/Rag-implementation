import logging
from ingest_portarias import IngestPortarias

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_database():
    """Função principal que executa o processo de ingestão."""
    try:
        logger.info("Iniciando processo de atualização da base de dados vetorial.")
        ingestor = IngestPortarias()
        ingestor.run_ingestion()
        logger.info("Processo de atualização finalizado com sucesso.")
    except Exception as e:
        logger.error(f"Ocorreu um erro crítico durante a atualização: {str(e)}", exc_info=True)

if __name__ == "__main__":
    update_database()