import os
import shutil


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
    # Έλεγχος αν το αρχείο υπάρχει
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
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

    # Μετακίνηση του αρχείου
    try:
        shutil.move(file_path, destination_path)
        print(f"✅ File moved successfully to: {destination_path}")
    except Exception as e:
        print(f"❌ Error while moving file: {e}")

def restore():
    with open('quar_id.txt') as f:
        quar_id = f.readline().strip()

    files = os.listdir(os.getcwd())
    if files:
        file = files[0]  # Παίρνουμε το πρώτο αρχείο που βρίσκουμε στον τρέχοντα φάκελο
        shutil.move(file, os.path.join(quar_id, file))
    else:
        print("No files to restore.")

def folder_creator():
    dir_path = r"Extracted_txts"

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
        print("Directory created successfully!")


    return dir_path


if __name__ == '__main__':
    main()
