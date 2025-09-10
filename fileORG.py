from tkinter import *
from tkinter import filedialog, messagebox, PhotoImage
import customtkinter as ctk
import os
import shutil
import hashlib
from collections import defaultdict

from numpy.ma.core import left_shift

root = ctk.CTk()
ctk.set_appearance_mode("Dark") # set appearance to dark mode
ctk.set_default_color_theme("blue") # set theme to blue
root.title("FileORG")
root.geometry("1000x600")
root.configure(background="#1f1f1f")
root.iconbitmap("fileORG.ico")

folder_path = "" # define folder_path

def theme(choice):
    if choice == "Light":
        ctk.set_appearance_mode("Light")
    if choice == "Dark":
        ctk.set_appearance_mode("Dark")
    if choice == "System":
        ctk.set_appearance_mode("System")

# Func that use for select dir
def selectdir():
    global folder_path # use folder_path as global variable
    folder_path = filedialog.askdirectory(title="SELECT FOLDER") # popup a select menu
    if folder_path:
        path_label.configure(text=f"CURRENT DIRECTORY ▶ {folder_path}") # if folder_path then config(path_label) and show currentdir

def sortfile(): # Func that sort file from dictionary

    file_types = { # dictionary that show support extension
        "Image": ['.jpg', '.jpeg', '.png', '.gif'],
        "Sound": ['.mp3', '.wav'],
        "Videos": ['.mp4', '.mov', '.avi', '.webm']
    }
    if not folder_path: # if statement that check if folder_path not select
        messagebox.showwarning("Warning", "Please select folder path") # then show this message
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

# --- Select button ---
selectbtn = ctk.CTkButton(root, text="SELECT FOLDER", corner_radius=8, fg_color=["#0c74ba","#343a40"], hover_color=["#0d344e","#0c74ba"], font=("Calibri",15), command=selectdir)
selectbtn.place(x = 10, y = 560)

# --- Label of Selected path ---
path_label = ctk.CTkLabel(root, text="PLEASE SELECT FOLDER FIRST", text_color = ["#262626","white"], corner_radius=8, fg_color=["#999999","#6c757d"], font=("Calibri",12))
path_label.place(x = 155, y = 560)

# --- Create tabview setting ---
tabview_setting = ctk.CTkTabview(root,width=300,height=550,)
tabview_setting.place(x = 670, y = 20)

    # --- Add tabview_setting page's ---
tab_whatnew = tabview_setting.add("What's New")
tab_setting = tabview_setting.add("Setting")
tab_about = tabview_setting.add("About")

        # --- What's New Page ---
NameApp = ctk.CTkLabel(tab_whatnew, text="FileORG",  text_color=["#262626","white"], font=("Impact", 40)) #FileORG
NameApp.place(x=81,y=5)

ver_label = ctk.CTkLabel(tab_whatnew, text="2.0.0-alpha", text_color=["#262626","white"], font=("Calibri",18)) #Version
ver_label.place(x=0,y=65)

note = ("   We're excited to announce a major update for our"
        "\napplication! In this new version, we've completely"
        "\noverhauled the user interface to bring you a modern"
        "\nand intuitive experience."
        "\n\n   Refreshed GUI: We've switched from the"
        "\nstandard Tkinter to CustomTkinter, giving "
        "\nthe program a more modern and polished look."
        "\n\n   Added Tabview: The application now features an"
        "\neasy-to-use tab menu that organizes content into"
        "\nthree main sections:"
        "\n\n     What's New: This tab provides a detailed"
        "\n     breakdown of all the new features and"
        "\n     improvements in this update, so you can stay"
        "\n     informed."
        "\n\n     Settings: You can now customize the app's"
        "\n     appearance by choosing between Dark, Light,"
        "\n     and System themes."
        "\n\n     About: This tab offers information about our"
        "\n     development team and details about the"
        "\n     application itself."
        )
patch_note = ctk.CTkLabel(tab_whatnew, text=note, justify="left")
patch_note.place(x=0, y=95)

        # --- Setting Page ---
setting_opt_theme = ctk.CTkOptionMenu(tab_setting,
                                      values=["Light", "Dark", "System"],
                                      command=theme,
                                      button_color=["#6c757d","#0c74ba"],
                                      button_hover_color=["#595959","#4297e4"],
                                      fg_color=["#0c74ba","#6c757d"],
                                      dropdown_hover_color="#0c74ba")
setting_opt_theme.set("Dark") #Set system to default
setting_opt_theme.place(x=75,y=10)

setting_label_theme = ctk.CTkLabel(tab_setting, text="Theme:", text_color="white", font=("Calibri",15))
setting_label_theme.place(x=10,y=10)


# --- Create tabview main ---
tabview_main = ctk.CTkTabview(root,width=600,height=450)
tabview_main.place(x = 30, y = 20)

    # --- Add tabview_main page's ---
tab_sort = tabview_main.add("Sorter")
tab_dupe = tabview_main.add("Duplicate Finder")

        # --- Sorter Page ---
sortbtn = ctk.CTkButton(tab_sort, text="SORT", text_color="white", corner_radius=8, fg_color=["#0c74ba","#343a40"], hover_color=["#0d344e","#0c74ba"], font=("Calibri",15), command=sortfile)
sortbtn.place(x = 224, y = 10)

        # --- Duplicate Finder Page ---
dupebtn = ctk.CTkButton(tab_dupe, text="FIND DUPE",  text_color="white", corner_radius=8, fg_color=["#0c74ba","#343a40"], hover_color=["#0d344e","#0c74ba"], font=("Calibri",15), command=find_dupe)
dupebtn.place(x = 224, y = 10)

root.resizable(0, 0)
root.mainloop()