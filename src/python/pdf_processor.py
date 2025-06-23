import fitz
import pytesseract
from PIL import Image
import io
import os
import logging
import re
from concurrent.futures import ThreadPoolExecutor


def extract_highlighted_text(page):
    """Extract text from highlighted areas in a PDF page."""
    highlights = []
    for annot in page.annots():
        if annot.type[0] == 8:  # 8 is the code for a highlight annotation
            rect = annot.rect
            text = page.get_textbox(rect).strip()
            if text:
                highlights.append(text)
    return highlights

def extract_title(text):
    """Extrai o título usando regex do texto da página"""
    pattern = re.compile(
        r'(?i)portaria\s+n[°º]?\s*\d+\s*\/\s*\d+\s*\/\s*mpc\s*\/\s*pa',
        flags=re.IGNORECASE
    )
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if pattern.search(line):
            return line
    return None

def process_single_pdf(pdf_path, output_dir):
    """Process a single PDF file, extracting the first page and highlighted text."""
    try:
        filename = os.path.basename(pdf_path)
        output_file = os.path.splitext(filename)[0] + '.txt'
        output_path = os.path.join(output_dir, output_file)
        
        # Open PDF
        with fitz.open(pdf_path) as pdf:
            text = ""
            title = ""
            if pdf.page_count > 0:  # Check if there is at least one page
                page = pdf[0]  # Get only the first page
                
                # Extrair texto nativo
                page_text = page.get_text()
                title = extract_title(page_text)
                
                # Se não encontrado, tentar OCR
                if not title:
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    ocr_text = pytesseract.image_to_string(img, lang='por')
                    title = extract_title(ocr_text)
                
                # Fallback para texto destacado
                if not title:
                    highlighted_text = extract_highlighted_text(page)
                    title = highlighted_text[0] if highlighted_text else "Sem título"
                
                page_text = page.get_text()
                
                # If no text found, use OCR
                if not page_text.strip():
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    page_text = pytesseract.image_to_string(img, lang='por')
                
                text += f"\n--- Página 1 ---\n{page_text}"
            
            # Save extracted text and title
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\nText: {text.strip()}")
                
            logging.info(f"Processed: {filename}")
            return {'filename': filename, 'title': title}
                    
    except Exception as e:
        logging.error(f"Error processing {filename}: {str(e)}")
        return {'filename': filename, 'title': 'Error'}
    
def process_pdfs(pdf_dir, output_dir, max_workers=3):
    """
    Process all PDFs in parallel and return titles
    """
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    total_files = len(pdf_files)
    logging.info(f"Starting to process {total_files} PDF files")
    
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
            
            if i % 5 == 0:  # Log progress every 5 files
                logging.info(f"Processing progress: {i}/{total_files} ({(i/total_files)*100:.1f}%)")
    
    logging.info(f"PDF processing completed. Successfully processed {success_count} of {total_files} files")
    return results