import fitz
import pytesseract
from PIL import Image
import io
import os
import logging
import re
from concurrent.futures import ThreadPoolExecutor
from langdetect import detect, LangDetectException

# --- AGENTE 1: Lógica de Verificação de Idioma ---
def is_portuguese(text: str) -> bool:
    """Verifica se o texto fornecido está em português."""
    try:
        # Usa uma amostra do texto para eficiência
        sample = text[:500] if len(text) > 500 else text
        if not sample.strip():
            return False
        # Retorna True se o idioma detectado for 'pt'
        return detect(sample) == 'pt'
    except LangDetectException:
        # Se a detecção falhar (texto muito curto ou confuso), descarta por segurança.
        logging.warning("Não foi possível detectar o idioma do texto.")
        return False

# --- INÍCIO DA CORREÇÃO ---
def extract_title_and_year(text):
    """Extrai o título e o ano da portaria usando regex."""
    # CORREÇÃO: Removido o flag inline (?i) para evitar o erro de compilação.
    # O argumento 'flags=re.IGNORECASE' já lida com a sensibilidade de maiúsculas/minúsculas.
    pattern = re.compile(
        r'(portaria\s+n[°º]?\s*\d+\s*\/\s*(\d{4})\s*\/\s*mpc\s*\/\s*pa)',
        flags=re.IGNORECASE
    )
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        match = pattern.search(line)
        if match:
            title = match.group(1)  # O título completo (1º grupo de captura)
            year = int(match.group(2)) # O ano (2º grupo de captura)
            return title, year
    return "Sem título", None
# --- FIM DA CORREÇÃO ---


def process_single_pdf(pdf_path, output_dir):
    """Processa um único PDF, aplicando o Agente 1 e extraindo metadados."""
    filename = os.path.basename(pdf_path)
    try:
        output_file = os.path.splitext(filename)[0] + '.txt'
        output_path = os.path.join(output_dir, output_file)
        
        with fitz.open(pdf_path) as pdf:
            if not pdf.page_count > 0:
                logging.warning(f"PDF vazio ou corrompido: {filename}")
                return {'filename': filename, 'title': 'Error', 'reason': 'PDF Vazio'}

            page = pdf[0]
            page_text = page.get_text()
            
            if not page_text.strip():
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes()))
                page_text = pytesseract.image_to_string(img, lang='por')
            
            # --- Aplicação do AGENTE 1 ---
            if not is_portuguese(page_text):
                logging.warning(f"Documento '{filename}' parece não estar em português e será descartado.")
                return {'filename': filename, 'title': 'Error', 'reason': 'Não está em português'}

            title, year = extract_title_and_year(page_text)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\n")
                f.write(f"Year: {year}\n")
                f.write(f"Text: {page_text.strip()}")
                
            logging.info(f"Processado: {filename}")
            return {'filename': filename, 'title': title, 'year': year}
                    
    except Exception as e:
        logging.error(f"Erro ao processar {filename}: {str(e)}")
        return {'filename': filename, 'title': 'Error', 'reason': str(e)}

def process_pdfs(pdf_dir, output_dir, max_workers=3):
    """
    Processa todos os PDFs em paralelo e retorna os títulos.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    total_files = len(pdf_files)
    logging.info(f"Iniciando o processamento de {total_files} arquivos PDF")
    
    results = []
    success_count = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                process_single_pdf,
                os.path.join(pdf_dir, pdf_file),
                output_dir
            )
            for pdf_file in pdf_files
        ]
        
        for i, future in enumerate(futures, 1):
            result = future.result()
            if result and result['title'] != 'Error':
                success_count += 1
                results.append(result)
            
            if i % 5 == 0:  # Log de progresso a cada 5 arquivos
                logging.info(f"Progresso do processamento: {i}/{total_files} ({(i/total_files)*100:.1f}%)")
    
    logging.info(f"Processamento de PDF concluído. {success_count} de {total_files} arquivos processados com sucesso")
    return results