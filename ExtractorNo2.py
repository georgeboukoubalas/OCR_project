import re
import fitz  # pip install pymupdf
import chardet  # pip install chardet
import pytesseract  # pip install pytesseract
import os
from pdf2image import convert_from_path  # pip install pdf2image
import shutil


def cleaning_text(text: str) -> str:
    """
    Cleans the input text by normalizing newlines, removing long lines of symbols or non-alphanumerics,
    repeated garbage sequences, fixing common OCR errors, cleaning extra whitespace, and stripping leading/trailing whitespace.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned text.
    """

    # Normalize newlines first
    text = re.sub(r"\r\n|\r", "\n", text)

    # Remove long lines of symbols or non-alphanumerics (fake dividers, OCR junk)
    text = re.sub(r"[^\w\s.,;:?!@%&/()\"'\[\]\-+=€$\u00a3<>|{}\n]", "", text)

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
        return pytesseract.image_to_string(image_path, lang=lang)
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ""


def folder_creator(destination_dir = "Extracted_text"):
    #Create a folder for extracted text

    current_directory = os.getcwd()
    destination_dir_path = os.path.join(current_directory, destination_dir)
    try:
        os.makedirs(destination_dir_path, exist_ok=True)
        print(f"Directory '{destination_dir}' created successfully")
    except OSError as error:
        print(f"Directory '{destination_dir}' can not be created. {error}")

    return destination_dir_path

def main():
    # Find tesseract.exe path (try system PATH first)
    #pytesseract.pytesseract.tesseract_cmd = r"C:\Users\georg\Downloads\My programs-project\llm data analysis project\tesseract.exe" #remove hardcoded path
    try:
        pytesseract.pytesseract.tesseract_cmd = shutil.which('tesseract') #find tesseract in PATH
        if pytesseract.pytesseract.tesseract_cmd is None:
            raise FileNotFoundError("Tesseract not found in PATH")
    except FileNotFoundError:
        print("Tesseract is not installed or not in your system's PATH.")
        tesseract_path = input("Please enter the full path to tesseract.exe: ")
        if os.path.exists(tesseract_path):
             pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            print("Invalid path to tesseract.  Exiting.")
            return


    pdf_path = input("PDF path: ")

    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        print("You may have entered the file path incorrectly.")
        return  # Exit the program
    else:
        print("File found successfully")

    encoding = detect_pdf_encoding(pdf_path)

    if encoding:
        print("🔍 Encoding detected: " + str(encoding))
    else:
        print("⚠️ Unable to automatically detect encoding.  Using utf-8 as default.")
        encoding = "utf-8"  # Use a default encoding

    file_name = input("Enter a file name (without extension): ")
    destination_dir_path = folder_creator()  # Create the destination directory first
    filename = file_name + ".txt"
    filename_path = os.path.join(destination_dir_path, filename) #create full path

    try:
        pages = convert_from_path(pdf_path, 350)

        with open(filename, "w", encoding=encoding, errors="replace") as file: #open file in current directory
            for page_num, img in enumerate(pages):
                text = image_to_text(img)

                text = cleaning_text(text)

                text = "\n".join([line for line in text.split("\n") if line.strip()])
                file.write(f'\n--- Page {page_num + 1} --- \n')
                file.write(text)

        shutil.move(filename, destination_dir_path) #move file to destination dir
        print(f"Extracted text saved to: {filename_path}")


    except Exception as e:
        print(f"An error occurred during PDF processing: {e}")


if __name__ == "__main__":
    main()