from PyPDF2 import PdfReader
import os
# Get all the PDF filenames.
pdfFiles = []
for filename in os.listdir('.'):
    if filename.endswith('.pdf'):
        pdfFiles.append(filename)
pdfFiles.sort(key/str.lower)
pdfWriter = PyPDF2.pdfFileWriter()
