import pathlib
from pdf2image import convert_from_path
import pytesseract
import os
import chardet
import fitz # PyMuPDF
from FileManager import move
import re

def cleaning_text(text: str):
    # Normalize newlines first
    text = re.sub(r"\r\n|\r", "\n", text)

    # Remove long lines of symbols or non-alphanumerics (fake dividers, OCR junk)
    text = re.sub(r"[^Α-Ωα-ωΆ-ώA-Za-z0-9\s.,;:?!@%&/()\"'\[\]\-+=€$£<>|{}\n]", "", text)

    # Remove repeated garbage sequences (e.g. "οοοοοο", "τττττ", etc.)
    text = re.sub(r"([^\W\d_])\1{3,}", r"\1", text)

    # Fix common OCR errors
    text = text.replace("|||", " | ")
    text = text.replace("||", " | ")
    text = text.replace(" .", ".")
    text = text.replace(" ,", ",")
    text = text.replace(" :", ":")
    text = text.replace(" ;", ";")
    text = text.replace("..", ".")

    # Clean extra whitespace
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\n\s*\n", "\n\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text

def detect_pdf_encoding(pdf_path):
    # open pdf
    doc = fitz.open(pdf_path)
    extracted_text = ""

    # extract text from all the pages
    for page in doc:
        extracted_text += page.get_text("text")

    # if text doesn't have word (it is an image)
    if not extracted_text.strip():
        return "the PDF doesn't have common text. Maybe it was scanned before!"

    # encoding detection
    encoding_detected = chardet.detect(extracted_text.encode())['encoding']
    return encoding_detected or "unable to find encoding."

def main():
    #Find tesseract.exe path
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\georg\Downloads\My programs-project\llm data analysis project\tesseract.exe"

    #Enter PDF path that you want  to copy
    pdf_path = input(r"Enter PDF file path: ")

    #check if file was found in path
    if not os.path.exists(pdf_path):
        print(f"file not found: {pdf_path}")
        print("You may write the file path incorrectly.")
        exit()
    else:
        print(f"file founded successfully")
        encoding = str(detect_pdf_encoding(pdf_path))
        #print("🔍encoding detection: " + encoding)

    #Enter the file name that final text will be wrote down
    file_name = input("Enter a file name: ")

    filename_path = r"C:\Users\georg\PycharmProjects\OCR_project\\" + file_name + ".txt"
    destination_dir_path = r"C:\Users\georg\PycharmProjects\OCR_project\Extracted_txts"

    # Convert PDF to a list of images
    pages = convert_from_path(pdf_path, 300)

    #Open file for writing
    with open(file_name + ".txt", "w", encoding=encoding, errors="replace") as file:
    # Extract word from every page
        for page_num, img in enumerate(pages):
            text = pytesseract.image_to_string(img, lang='ell+eng')
            #Clean the garbage from the text
            text = cleaning_text(text)
            #erase the empty lines
            text = "\n".join([line for line in text.split("\n") if line.strip()])
            file.write(f'\n--- Page {page_num + 1} --- \n')
            file.write(text)

    move(filename_path, destination_dir_path)


if __name__ == "__main__":
    main()