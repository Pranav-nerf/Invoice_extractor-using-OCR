# Invoice_extractor-using-OCR

# Invoice Processing Script

This project is a Python script that *reads invoice PDFs, extracts important details like invoice number, description, and price, and then exports them into an **Excel file*.  
It also supports *OCR* (Optical Character Recognition) for scanned invoices.

---

## Features
- Reads all .pdf files from the data/invoices/ folder.
- Extracts text using:
  - *PyPDF2* → if the PDF has searchable text.
  - *pytesseract (OCR)* → if the PDF is scanned as an image.
- Uses *regular expressions* to find:
  - Document Number
  - Description
  - Price
- Saves results into an *Excel file* (invoices.xlsx) inside data/output/.
- Logs all activities (info, warnings, errors) into logs/process.log.

---

## Requirements
Make sure you have the following installed:

- Python 3.8+
- Libraries:
  ```bash
  pip install PyPDF2 pdf2image pytesseract pandas openpyxl
