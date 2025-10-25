def main():
    destination_dir_path = folder_creator()
    choice = input("Would you like to (M)ove or (R)estore?: ")

    if choice.upper() == 'M':
        file_path = input("Enter the exact path of the file that you want to move: ")
        move(file_path, destination_dir_path)
        print("Done.")

    elif choice.upper() == 'R':
        restore()
        print("Done.")

    else:
        print("No valid option selected, closing...")


def move(file_path, destination_dir):
    import os
    import shutil
    from tkinter import messagebox

    # Έλεγχος αν το αρχείο υπάρχει
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        messagebox.showerror(title="Error", message=f"file not found!!!")
        return

    """# Δημιουργία του φακέλου προορισμού αν δεν υπάρχει
    if not os.path.isdir(destination_dir):
        try:
            os.makedirs(destination_dir)
            print(f"📁 Created destination directory: {destination_dir}")
        except Exception as e:
            print(f"❌ Failed to create directory: {e}")
            return"""

    # Απόσπαση του ονόματος του αρχείου από το πλήρες path
    file_name = os.path.basename(file_path)

    # Δημιουργία του πλήρους path προορισμού
    destination_path = os.path.join(destination_dir, file_name)
    messagebox.showinfo(title="Directory", message=f"Destination directory created: {destination_path}")
    # Μετακίνηση του αρχείου
    try:
        shutil.move(file_path, destination_path)
        messagebox.showinfo(title=file_name, message = f"✅ File moved successfully to: {destination_path}")
        #print(f"✅ File moved successfully to: {destination_path}")
    except Exception as e:
        messagebox.showinfo(title=file_name, message=f"❌ Error while moving file: {e}")
        #print(f"❌ Error while moving file: {e}")

def restore():
    import os
    import shutil

    with open('quar_id.txt') as f:
        quar_id = f.readline().strip()

    files = os.listdir(os.getcwd())
    if files:
        file = files[0]  # Παίρνουμε το πρώτο αρχείο που βρίσκουμε στον τρέχοντα φάκελο
        shutil.move(file, os.path.join(quar_id, file))
    else:
        print("No files to restore.")

def folder_creator():
    from tkinter import messagebox
    import os

    dir_path = r"Extracted_txts"

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
        print("Directory created successfully!")
        messagebox.showinfo(title="Directory", message=f"Directory Extracted_txts created successfully!")

    return dir_path


if __name__ == '__main__':
    main()
