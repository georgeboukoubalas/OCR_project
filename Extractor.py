from pdf2image import convert_from_path
import pytesseract
import chardet
import fitz # PyMuPDF
from FileManager import move, folder_creator
from ExtractorManager import preprocessing, postprocessing, cleaning_text, crop_to_roi, process_txt_with_characterspliting
import os
from tkinter import *
from tkinter import messagebox

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
    pdf_path = PDF_Path_entry.get().replace('"', '').replace("'", '')
    if not pdf_path:
        messagebox.showerror("Oops", "Please make sure that you haven't left any fields empty!!!")
    #check if file was found in path
    elif not os.path.exists(pdf_path):
        messagebox.showerror(title="Error", message=f"file not found: {pdf_path}\nYou may write the file path incorrectly.")
        PDF_Path_entry.delete(0, END)
    else:
        messagebox.showinfo(title=pdf_path, message=f"File detected: {pdf_path}" )
        encoding = str(detect_pdf_encoding(pdf_path))
        #print("🔍encoding detection: " + encoding)

        #Enter the file name that final text will be wrote down
        file_name = File_Name_entry.get()


        filename_path = r"C:\Users\georg\PycharmProjects\OCR_project\\" + file_name + ".txt"
        destination_dir_path = folder_creator()

        # Convert PDF to a list of images
        pages = convert_from_path(pdf_path, 400)

        try:
            #Open file for writing
            with open(file_name + ".txt", "w", encoding=encoding, errors="replace") as file:
            # Extract word from every page
                for page_num, pil_img in enumerate(pages):

                    #crop the image to the region of interest (ROI)
                    cropped = crop_to_roi(pil_img)

                    #Extract text from the image
                    text = image_to_text(cropped)

                    #Clean the garbage from the text
                    text = cleaning_text(text)

                    #erase the empty lines
                    text = "\n".join([line for line in text.split("\n") if line.strip()])
                    file.write(f'\n--- Page {page_num + 1} --- \n')
                    file.write(text)

            process_txt_with_characterspliting(filename_path, encoding)
            move(filename_path, destination_dir_path)
        except FileNotFoundError:
            # I do not Know why but the message box below doesn't work need fix, fake FileNotFoundError occure but the code in try is steel worked ???
            # messagebox.showinfo(title="Error", message="Oops!!! \nSeems you might be used invalid characters in files name \nPlease make no use of characters like / , // , * ")
            File_Name_entry.delete(0, END)
            move(filename_path, destination_dir_path)

window = Tk()
window.title("Pdf To Text")
window.config(padx=30, pady=30)

# Labels
PDF_Path_label = Label(text="Enter PDF Path:")
PDF_Path_label.grid(row=1, column=0)
File_Name_label = Label(text="Enter File Name:")
File_Name_label.grid(row=2, column=0)

# Entries
PDF_Path_entry = Entry(width=40)
PDF_Path_entry.grid(row=1, column=1, columnspan=1)
PDF_Path_entry.focus()
File_Name_entry = Entry(width=40)
File_Name_entry.grid(row=2, column=1, columnspan=1)

# Buttons
submit_button = Button(text="Submit", width=30, command=main)
submit_button.grid(row=3, column=1)

# Run
window.mainloop()