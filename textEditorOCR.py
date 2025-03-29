fileName = str(input("Enter file name: "))
with open(fileName + ".txt", "w") as file:
    file.write("Hello, this is a text file!")
