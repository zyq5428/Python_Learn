from PyPDF2 import PdfReader

reader = PdfReader("automate\meetingminutes.pdf")
text = ""
for page_num in range(len(reader.pages)):
    page =  reader.pages[page_num]
    text = page.extract_text()
    print(text)