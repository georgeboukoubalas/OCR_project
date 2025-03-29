from pdf2image import convert_from_path
import pytesseract

#Find tesseract.exe path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\georg\Downloads\My programs-project\llm data analysis project\tesseract.exe"

#Enter PDF path that you want  to copy
PDFpath = str(input(r"Enter PDF file path: "))
# "C:\Users\georg\Downloads\OG Έγγραφα\100DaysOfPython\pdf&others\Syllabus+for+100+Days+of+Python.pdf"

#Enter the file name that final text will be wrote down
fileName = str(input("Enter file name: "))

# Convert PDF to a list of images
pages = convert_from_path(PDFpath, 300)

#Open file for writing
with open(fileName + ".txt", "w") as file:
# Extract word from every page
    for page_num, img in enumerate(pages):
        text = pytesseract.image_to_string(img, lang='eng')
        #erase the empty lines
        text = "\n".join([line for line in text.split("\n") if line.strip()])
        file.write(f'--- Page {page_num + 1} ---\n')
        file.write(text)
