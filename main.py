import os, re, base64
import tkinter as tk
from tkinter import Label, filedialog as fd
from tkinter import ttk
from urllib.parse import unquote

class OneHTML:
    def __init__(self):
        self.fileinfo = {
            "dirpath": "",
            "filepathbase": "",
            "filepathtype": ""
        }
        self.lines = []
        self.fgok = "blue"
        self.fgsuccess = "green"
        self.fgfail = "red"
        

    def getStyles(self):
        """Extracts styles from the HTML content."""
        styles = ""
        found = False
        filename = os.path.join(self.fileinfo["filepathbase"], self.fileinfo["filepathbase"])
        for entry in os.listdir(self.fileinfo["dirpath"]):
            # Construct the full path to check if it's a directory
            full_path = os.path.join(self.fileinfo["dirpath"] , entry)
            if os.path.isdir(full_path) and entry[:len(self.fileinfo["filepathbase"])] == self.fileinfo["filepathbase"]:
                subfiles = os.listdir(os.path.join(self.fileinfo["dirpath"], entry))
                for i, sub in enumerate(subfiles):
                    if re.search(r".*\.css", sub):
                        with open(os.path.join(self.fileinfo["dirpath"], entry, sub), 'r') as file:
                            styles += "\n/* "+entry+" */\n"+file.read()+"\n"
        
        for i, line in enumerate(lines):
            if re.search(r"</style>", line):
                lines[i] = re.sub(r"</style>", f"{styles}</style>", line)
                found = True
                break
        if not found and len()(styles) > 0:
            for i, line in enumerate(lines):
                if re.search(r"</head>", line):
                    lines[i] = re.sub(r"</head>", f"{styles}</head>", line)
                    break
        
    def convertImage(self, imgname, line):
        """Converts an image to a base64 string and replaces the source in the HTML content."""
        new_img = ""
        imgpath = unquote(os.path.join(self.fileinfo["dirpath"], imgname))
        if os.path.isfile(imgpath):
            with open(imgpath, "rb") as imgf:
                encoded_string = base64.b64encode(imgf.read()).decode('utf-8')
                new_src = f"data:image/{self.fileinfo['filepathtype']};base64,{encoded_string}"
                new_img = re.sub(f"<img (.*)src=\"{imgname}\" ", f"<img \\1src=\"{new_src}\" ", line, flags=re.IGNORECASE)
        return new_img

    def convline(self,line):
        """Converts a single line by replacing image source."""
        pattern = "<img .*src=\"(.+)\" "
        newline = line
        m = re.search(pattern, line, re.IGNORECASE)
        if m:
            group_count = len(m.groups())
            for i in range(group_count):
                imgname = m.group(i+1)
                replacement = self.convertImage(imgname, line)
                newline = re.sub(pattern, replacement, line, count=0, flags=re.IGNORECASE)
        return newline

    def open_file_dialog(self):
        # This function will be called when the "Open File" button is clicked
        file_path = fd.askopenfilename(
            title="Open a file",
            initialdir="/", # Start in the root directory (adjust as needed)
            filetypes=(("HTML Files", "*.html"), ("All Files", "*.*")) # Filter file types
        )
        if file_path:
            self.fileinfo["dirpath"] = "/".join(file_path.split("/")[:-1]) # Get the directory path from the file path
            self.fileinfo["filepathbase"] = "".join(file_path.split("/")[-1].split(".")[:-1]) # Get the file name from the path
            self.fileinfo["filepathtype"] = file_path.split(".")[-1] # Get the file extension from the path
            self.fileinfo["filename"] = file_path.split("/")[-1] # Get the filename from the path

            with open(file_path, 'r') as file:
                global lines
                lines = [line.rstrip() for line in file]
                pattern = "<img .*src=\"(.+)\" "

                for i, line in enumerate(lines):
                    m = re.search(pattern, line, re.IGNORECASE)
                    if m:
                        group_count = len(m.groups())
                        for i in range(group_count):
                            imgname = m.group(i+1)
                            replacement = self.convertImage(imgname, line)
                            lines[i] = re.sub(pattern, replacement, line, count=0, flags=re.IGNORECASE)

            self.getStyles()
            outpath = os.path.join(self.fileinfo["dirpath"], f"{self.fileinfo['filepathbase']}_CONVERTED.{self.fileinfo['filepathtype']}")
            with open(outpath, 'w') as f:
                for i, line in enumerate(lines):
                    line = self.convline(line)
                    f.write(f"{line}\n")
            lbtext="The file converted!"
            fgcolor=self.fgsuccess
        else:
            lbtext="No file selected!"
            fgcolor=self.fgfail
        self.lb.config(text=lbtext, font =("Courier", 10), fg=fgcolor)


    def main(self):
        self.root = tk.Tk()
        self.root.title("Make it one HTML file!")
        self.root.geometry("300x100")


        self.root.update_idletasks()  # ensures geometry is calculated

        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        la = Label(self.root, text = "Convert your HTML file\nto a single!")
        la.config(font =("Courier", 14), fg=self.fgok)

        open_button = ttk.Button(
            self.root,
            text="Open File",
            command=self.open_file_dialog # Pass the function reference, not the result of calling it
        )

        self.lb = Label(self.root, text = "")

        la.pack()
        open_button.pack(expand=True)
        self.lb.pack()

        self.root.mainloop()

if __name__ == "__main__":
    one_html = OneHTML()
    one_html.main()
