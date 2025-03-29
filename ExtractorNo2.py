from pdf2image import convert_from_path
import pytesseract

#Find tesseract.exe path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\georg\Downloads\My programs-project\llm data analysis project\tesseract.exe"

pages = convert_from_path(r"C:\Users\georg\Downloads\OG Έγγραφα\100DaysOfPython\pdf&others\Syllabus+for+100+Days+of+Python.pdf", 300)

for page_num, img in enumerate(pages):
    text = pytesseract.image_to_string(img, lang='eng')

    text = "\n".join([line for line in text.split("\n") if line.strip()])

    print(f'--- page {page_num + 1} ---')
    print(text)
