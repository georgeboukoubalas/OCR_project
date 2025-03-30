import fitz  # PyMuPDF
import chardet
import os

def detect_pdf_encoding(pdf_path):
    # Άνοιγμα PDF
    doc = fitz.open(pdf_path)
    extracted_text = ""

    # Εξαγωγή κειμένου από όλες τις σελίδες
    for page in doc:
        extracted_text += page.get_text("text")

    # Αν το PDF δεν έχει κείμενο (είναι εικόνες)
    if not extracted_text.strip():
        return "Το PDF δεν περιέχει κανονικό κείμενο. Ίσως είναι σκαναρισμένο!"

    # Ανίχνευση encoding
    encoding_detected = chardet.detect(extracted_text.encode())['encoding']
    return encoding_detected or "Αδύνατη η ανίχνευση encoding."

# Δοκιμή με το PDF σου
pdf_path = str(input(r"Enter PDF file path: "))
if os.path.exists(pdf_path):
    print("PDF open correctly!")
    encoding = detect_pdf_encoding(pdf_path)
    print(f"🔍encoding detection: {encoding}")
else:
    print("test.pdf not found.")

'''#check if the pdf was found correctly
if os.path.exists(file_path):
    print("✅ Το PDF ανοίχτηκε σωστά!")

    # encode detector
    with open(file_path, "rb") as f:
        raw_data = f.read()
    encoding_detected = chardet.detect(raw_data)['encoding']

    print(f"🔍 Ανιχνεύθηκε encoding: {encoding_detected}")

    with open(file_path, "r", encoding=encoding_detected, errors="replace") as file:
        text = file.read()
    print(text)
else:
    print("❌ Το test.pdf δεν βρέθηκε.")
'''
