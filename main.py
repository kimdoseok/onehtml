from ast import pattern
import os
import tkinter as tk
from tkinter import Label, filedialog as fd
from tkinter import ttk
import re

lines = []
fileinfo = {"filepathbase": "", "filepathtype": "", "dirpath": ""}
root = tk.Tk()
la = Label(root, text = "")

def getStyles(dirpath, basename):
    """Extracts styles from the HTML content."""
    styles = ""
    found = False
    for entry in os.listdir(dirpath):
        # Construct the full path to check if it's a directory
        full_path = os.path.join(dirpath, entry)
        if os.path.isdir(full_path) and entry[:len(basename)] == basename:
            subfiles = os.listdir(os.path.join(dirpath, entry))
            for i, sub in subfiles:
                if re.search(r".*\.css", sub):
                    with open(os.path.join(dirpath, entry, sub), 'r') as file:
                        styles += "\n"+file.read()+"\n"
    for i, line in enumerate(lines):
        if re.search(r"</style>", line):
            lines[i] = re.sub(r"</style>", f"{styles}</style>", line)
            break

def convertImage(imgname):
    """Converts an image to a base64 string and replaces the source in the HTML content."""
    imgpath = os.path.join(fileinfo["dirpath"], imgname)
    new_img = ""
    with open(imgpath, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        new_src = f"data:image/{fileinfo['filepathtype']};base64,{encoded_string}"
        for i, line in enumerate(lines):
            if re.search(f"<img .*src=\"{imgname}\" ", line, re.IGNORECASE):
                lines[i] = re.sub(f"<img (.*)src=\"{imgname}\" ", f"<img \\1src=\"{new_src}\" ", line, flags=re.IGNORECASE)
                break
    return new_img

def convline(line):
    """Converts a single line by replacing image source."""
    pattern = "<img .*src=\"(.+)\" "
    m = re.search(pattern, line, re.IGNORECASE)
    if m:
        imgname = m.group(1)
        print(f"Extracted value: {imgname}")
        convertImage(imgname)        
    re.sub(pattern, replacement, string, count=0, flags=0)
    text = "My phone number is 123-456-7890. Another is 987-654-3210."
    pattern = r"\d{3}-\d{3}-\d{4}" # Pattern for a phone number
    replacement = "[REDACTED]"

    updated_text = re.sub(pattern, replacement, text)
    print(updated_text)
    # Output: My phone number is [REDACTED]. Another is [REDACTED].



    return newline

def addStyle():
    """Adds a style tag to the HTML content."""
    found = False
    for i, line in enumerate(lines):
        if re.search(r"</style>", line)
    style = "<style>img{max-width:100%;height:auto;}</style>"
    lines.insert(1, style) # Insert the style tag after the opening <head> tag

def open_file_dialog():
    """Opens a file dialog and convert the selected file."""
    file_path = fd.askopenfilename(
        title="Open a file",
        initialdir="/", # Start in the root directory (adjust as needed)
        filetypes=(("HTML Files", "*.html"), ("All Files", "*.*")) # Filter file types
    )
    if file_path:
        print("Selected file:", file_path)
        global fileinfo, lines
        fileinfo["dirpath"] = "/".join(file_path.split("/")[:-1]) # Get the directory path from the file path
        fileinfo["filepathbase"] = "".join(file_path.split("/")[-1].split(".")[:-1]) # Get the file name from the path
        fileinfo["filepathtype"] = file_path.split(".")[-1] # Get the file extension from the path

        with open(file_path, 'r') as file:
            global lines
            lines = [line.rstrip() for line in file]
        print("Directory path:", fileinfo["dirpath"])
        print("File name:", fileinfo["filepathbase"])
        print("File extension:", fileinfo["filepathtype"])
        la.config(text="The file converted!")
    else:
        la.config(text="No file selected!")

def main():
    """Main function to run the application."""
    pass # The main function is not needed in this context as we are using Tkinter's event loop
    # Create the main application window
    global root,la
    root = tk.Tk()
    root.title("Make it one HTML file!")
    root.geometry("300x150")

    l = Label(root, text = "Convert your HTML file\nto a single!")
    l.config(font =("Courier", 14))

    # Create an "Open File" button
    open_button = ttk.Button(
        root,
        text="Open File",
        command=open_file_dialog # Pass the function reference, not the result of calling it
    )

    la = Label(root, text = "")
    la.config(font =("Courier", 10), fg="red")

    l.pack()
    open_button.pack(expand=True)
    la.pack()
        
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
     main()