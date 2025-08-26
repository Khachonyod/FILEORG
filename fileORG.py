from tkinter import *
from tkinter import filedialog, messagebox, PhotoImage
import os
import shutil
import hashlib
from collections import defaultdict

root = Tk()
root.title("FileORG")
root.geometry("1000x600")
root.configure(background="#1f1f1f")
root.iconbitmap("fileORG.ico")

folder_path = ""

def selectdir():
    global folder_path
    folder_path = filedialog.askdirectory(title="SELECT FOLDER")
    if folder_path:
        path_label.config(text=f"CURRENT DIRECTORY ▶ {folder_path}", bg="#1f1f1f")

def sortfile():

    file_types = {
        "Image": ['.jpg', '.jpeg', '.png', '.gif'],
        "Sound": ['.mp3', '.wav'],
        "Videos": ['.mp4', '.mov', '.avi', '.webm']
    }
    if not folder_path:
        messagebox.showwarning("Warning", "Please select folder path")
        return

    yon2 = messagebox.askyesno(title="Do you want to proceed.", message="Press yes if you want to proceed.")
    if yon2:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()

                if filename.lower() == "desktop.ini":
                    continue

                for folder, extension in file_types.items():
                    if ext in extension:
                        target_dir = os.path.join(folder_path, folder)
                        os.makedirs(target_dir, exist_ok=True)
                        shutil.move(file_path, target_dir)
                        break

        path_label.config(text="FINISHED!!")


def get_file_hash(path, block_size=65536):
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        buf = f.read(block_size)
        while buf:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def find_dupe():
    global folder_path
    if not folder_path:
        messagebox.showwarning("Warning", "Please select folder path")
        return
    hash_dict = defaultdict(list)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)

            try:
                file_hash = get_file_hash(filepath)
                hash_dict[file_hash].append(filepath)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

    duplicate = {}
    for h, path in hash_dict.items():
        if len(path) > 1:
            duplicate[h] = path

    if duplicate:
        msg = "Do yo want to proceed.\n"
        for h, paths in duplicate.items():
            msg += f"Hash: {h}\n"
            for p in paths:
                msg += f"Path: {p}\n"
        yon1 = messagebox.askyesno(title="Duplicate found", message="Found duplicate file, " + msg)
        if yon1:
            chosedelfiles = filedialog.askopenfilenames(
                title="Select one or multiple file",
            )
            for chosedelfile in chosedelfiles:
                try:
                    os.remove(chosedelfile)
                except Exception as e:
                    messagebox.showerror("Error: 102", f"Can't remove {chosedelfile}: {e}")
    else:
        messagebox.showinfo(title="No duplicate files found.", message="Scan complete. No duplicate files were found.")

NameApp = Label(
                root,
                text="FileORG",
                fg="white",
                bg="#1f1f1f",
                font=("Impact", 40)
                )
NameApp.place(x = 425, y = 10)

cfbtn = Button(
                root,
                text="SELECT FOLDER",
                fg="white",
                bg="green",
                font=("Tahoma",10),
                command=selectdir
                )
cfbtn.place(x = 10, y = 560)

sortbtn = Button(
                root,
                text="SORT",
                fg="white",
                bg="green",
                font=("Tahoma",10),
                command=sortfile
                )
sortbtn.place(x = 10, y = 530)

dupebtn = Button(
                root,
                text="FIND DUPE",
                fg="white",
                bg="green",
                font=("Tahoma",10),
                command=find_dupe
                )
dupebtn.place(x = 55, y = 530)

path_label = Label(
                root,
                text="PLEASE SELECT FOLDER FIRST",
                fg="white",
                bg="#1f1f1f",
                relief="sunken",
                font=("Tahoma",12)
                )
path_label.place(x = 120, y = 561)

ver_label = Label(
                text="1.1.1-alpha",
                fg="grey",
                bg="#1f1f1f",
                font=("Tahoma",12)
                )
ver_label.place(x = 900, y = 7)

root.resizable(0, 0)
root.mainloop()