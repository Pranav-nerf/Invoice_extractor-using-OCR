import os
import re
import logging
import pandas as pd
import PyPDF2
from pdf2image import convert_from_path
import pytesseract

INVOICE_FOLDER = "data/invoices/"
OUTPUT_FOLDER = "data/output/"
LOG_FILE = "logs/process.log"

PATTERNS = {
    "document_number": r"Document\s*No[:\-]?\s*(\d+)",
    "description": r"Description[:\-]?\s*(.+)",  
    "price": r"Price[:\-]?\s*\$?([\d,.]+)"        
}
def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
def read_pdfs():
    pdf_texts = {}
    for file in os.listdir(INVOICE_FOLDER):
        if file.endswith(".pdf"):
            path = os.path.join(INVOICE_FOLDER, file)
            try:
                text = extract_text_from_pdf(path)
                if not text.strip():
                    logging.warning(f"No text found in {file}, using OCR...")
                    text = extract_text_with_ocr(path)
                pdf_texts[file] = text
                logging.info(f"Processed {file}")
            except Exception as e:
                logging.error(f"Error reading {file}: {e}")
    return pdf_texts
def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text
def extract_text_with_ocr(path):
    text = ""
    images = convert_from_path(path)
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text
def parse_invoice(text):
    data = []
    for field, pattern in PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[field] = match.group(1).strip()
            logging.info(f"extracted {field}: {data[field]}")
        else:
            data[field] = None
            logging.warning(f"Could not find {field}")
    return data
def export_to_excel(data_list, filename="invoices.xlsx"):
    try:
        df = pd.DataFrame(data_list)
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        df.to_excel(output_path, index=False)
        logging.info(f"exported data to {output_path}")
        print(f"data exported to {output_path}")
    except Exception as e:
        logging.error(f"error exporting data: {e}")
def main():
    setup_logging()
    logging.info("starting invoice processing...")
    pdfs = read_pdfs()
    parsed_data = []
    for filename, text in pdfs.items():
        invoice_data = parse_invoice(text)
        invoice_data["filename"] = filename
        parsed_data.append(invoice_data)

    export_to_excel(parsed_data)
    logging.info("processing completed.")

if __name__ == "__main__":
    main()