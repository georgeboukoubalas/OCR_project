from pdf2image import convert_from_path

images = convert_from_path(r"C:\Users\georg\Downloads\OG Έγγραφα\100DaysOfPython\pdf&others\Syllabus+for+100+Days+of+Python.pdf", poppler_path=r"C:\Users\georg\Release-24.08.0-0\poppler-24.08.0\Library\bin")

for img in images:
    img.show()
