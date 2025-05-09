from pdf2image import convert_from_path
import pytesseract
import chardet
import fitz # PyMuPDF
from FileManager import move, folder_creator
from ExtractorManager import preprocessing, postprocessing, cleaning_text, crop_to_roi
import os

def detect_pdf_encoding(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        extracted_text = ""

        for page in doc:
            extracted_text += page.get_text("text")

        if not extracted_text.strip():
            return None  # Indicate no text found

        encoding_detected = chardet.detect(extracted_text.encode())['encoding']
        return encoding_detected
    except Exception as e:
        print(f"Error detecting encoding: {e}")
        return None

def image_to_text(image_path, lang='ell+eng'):
    try:
        custom_config = r'--oem 1 --psm 3'
        return pytesseract.image_to_string(image_path, lang=lang, config=custom_config)
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ""


def main():
    #pytesseract version: python -c "import pytesseract; print(pytesseract.__version__)"

    #Find tesseract.exe path
    #pytesseract.pytesseract.tesseract_cmd = r"C:\Users\georg\Downloads\My programs-project\llm data analysis project\tesseract.exe"
    #pytesseract.pytesseract.tesseract_cmd = r".\tesseract.exe"

    #Enter PDF path that you want  to copy
    #pdf_path = input(r"Enter PDF file path: ")
    pdf_path = input(r"PDF path: ")
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
    destination_dir_path = folder_creator()

    # Convert PDF to a list of images
    pages = convert_from_path(pdf_path, 400)

    #Open file for writing
    with open(file_name + ".txt", "w", encoding=encoding, errors="replace") as file:
    # Extract word from every page
        for page_num, pil_img in enumerate(pages):

            #bw = preprocessing(pil_img)
            cropped = crop_to_roi(pil_img)
            #Extract text from the image
            text = image_to_text(cropped)

            #Clean the garbage from the text
            text = cleaning_text(text)
            #text = postprocessing(text)

            #erase the empty lines
            text = "\n".join([line for line in text.split("\n") if line.strip()])
            file.write(f'\n--- Page {page_num + 1} --- \n')
            file.write(text)

    move(filename_path, destination_dir_path)

if __name__ == "__main__":
    main()
