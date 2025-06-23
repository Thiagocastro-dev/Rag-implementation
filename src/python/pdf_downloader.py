import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging
import re

def get_pdf_links_first_page(base_url):
        """Get PDF links only from the first page"""
        pdf_links = set()
    
        # Configure session for better performance
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
        try:
            logging.info(f"Fetching first page: {base_url}")
            
            response = session.get(base_url, timeout=60)
            response.raise_for_status()
    
            soup = BeautifulSoup(response.text, 'html.parser')
    
            # Find PDF links on the page (both direct and indirect links)
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if href.endswith('.pdf') or 'download' in href.lower():
                    full_link = urllib.parse.urljoin(base_url, href)
                    pdf_links.add(full_link)
    
            logging.info(f"Found {len(pdf_links)} PDF links on the first page.")
            
        except Exception as e:
            logging.error(f"Error fetching the first page: {str(e)}")
        
        return list(pdf_links)
    
def download_pdf(session, base_url, pdf_link, output_dir):
        """Download a single PDF file"""
        try:
            # Clean filename and create full URL
            filename = os.path.basename(urllib.parse.unquote(pdf_link))
            filename = re.sub(r'[^\w\-_\.]', '_', filename)
            if not filename.endswith('.pdf'):
                filename += '.pdf'
                
            full_url = urllib.parse.urljoin(base_url, pdf_link)
            output_path = os.path.join(output_dir, filename)
            
            # Skip if file already exists
            if os.path.exists(output_path):
                logging.info(f"File already exists: {filename}")
                return True
            
            logging.info(f"Downloading: {full_url}")
            response = session.get(full_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Verify it's actually a PDF
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' not in content_type and 'octet-stream' not in content_type:
                logging.warning(f"Skipping non-PDF content: {full_url}")
                return False
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logging.info(f"Successfully downloaded: {filename}")
            return True
            
        except Exception as e:
            logging.error(f"Error downloading {pdf_link}: {str(e)}")
            return False
    
def download_pdfs_first_page(url, output_dir):
        """
        Download all PDFs from the first page of a webpage
        """
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Configure session
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            # Get PDF links from the first page
            pdf_links = get_pdf_links_first_page(url)
            total_pdfs = len(pdf_links)
            logging.info(f"Found {total_pdfs} unique PDF files to download from the first page.")
            
            if not pdf_links:
                logging.error("No PDF links found!")
                return 0
            
            # Download PDFs sequentially
            success_count = 0
            for i, pdf_link in enumerate(pdf_links, 1):
                if download_pdf(session, url, pdf_link, output_dir):
                    success_count += 1
                
                if i % 50 == 0:
                    logging.info(f"Progress: {i}/{total_pdfs} ({(i/total_pdfs)*100:.1f}%)")
            
            logging.info(f"Download completed. Successfully downloaded {success_count} of {total_pdfs} PDFs.")
            return success_count
            
        except Exception as e:
            logging.error(f"Error in download process: {str(e)}")
            return 0
