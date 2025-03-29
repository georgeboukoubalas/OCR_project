from pdf2image import convert_from_path
import pytesseract

#Find tesseract.exe path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\georg\Downloads\My programs-project\llm data analysis project\tesseract.exe"

# Μετατροπή του PDF σε λίστα εικόνων
pages = convert_from_path(r"C:\Users\georg\Downloads\OG Έγγραφα\100DaysOfPython\pdf&others\Syllabus+for+100+Days+of+Python.pdf", 300)

# Εξαγωγή κειμένου από κάθε σελίδα
for page_num, img in enumerate(pages):
    text = pytesseract.image_to_string(img, lang='eng')

    # Αφαίρεση κενών γραμμών
    text = "\n".join([line for line in text.split("\n") if line.strip()])

    print(f'--- Σελίδα {page_num + 1} ---')
    print(text)
