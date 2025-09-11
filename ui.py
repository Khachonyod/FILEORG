import os
import shutil
import customtkinter as ctk
import time

from customtkinter import CTkButton, CTkLabel, set_appearance_mode, CTkTabview, CTkScrollableFrame, CTkOptionMenu
from tkinter import filedialog, messagebox
from logic import FileLogic
from collections import defaultdict


class FileORGApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("1000x600")
        self.resizable(0, 0)
        set_appearance_mode("Dark")

        self.logic = FileLogic()

        self.folder_path = ""


        self.curr = time.time()
        self.curr = time.ctime(self.curr)

# ==================== UI ====================

        self.select_folder_btn = CTkButton(self, text="SELECT FOLDER", text_color=["#262626","white"], corner_radius=8, fg_color=["#0c74ba","#343a40"], hover_color=["#0d344e","#0c74ba"], font=("Calibri",15), command=self.select_folder)
        self.select_folder_btn.place(x=10, y=560)

        self.path_label = CTkLabel(self, text="PLEASE SELECT FOLDER FIRST", text_color=["#262626","white"], corner_radius=8, fg_color=["#999999","#6c757d"], font=("Calibri",15))
        self.path_label.place(x=155, y=560)

        # === Create tabview setting ===
        self.tabview_setting = ctk.CTkTabview(self, width=300, height=550, )
        self.tabview_setting.place(x=670, y=20)

        # --- Tabview setting add ---
        self.tab_whatnew = self.tabview_setting.add("What's New")
        self.tab_setting = self.tabview_setting.add("Setting")
        self.tab_about = self.tabview_setting.add("About")

        #***WHAT"S NEW***
        self.patch_note = CTkLabel(self.tab_whatnew, text=self.logic.note, justify="left", font=("Calibri",12))
        self.patch_note.place(x=0, y=95)
        self.nameapp = CTkLabel(self.tab_whatnew, text="FileORG", text_color=["#262626","white"], font=("Impact", 40))
        self.nameapp.place(x=81,y=5)
        self.ver_label = CTkLabel(self.tab_whatnew, text="2.0.0-alpha", text_color=["#262626", "white"], font=("Calibri", 18))  # Version
        self.ver_label.place(x=0, y=65)
        # ***SETTING***
        self.setting_opt_theme = CTkOptionMenu(self.tab_setting, values=["Light", "Dark", "System"], command=self.logic.theme,  button_color=["#6c757d","#0c74ba"], button_hover_color=["#595959","#4297e4"], fg_color=["#0c74ba","#6c757d"], dropdown_hover_color="#0c74ba")
        self.setting_opt_theme.set("Dark")
        self.setting_opt_theme.place(x=75,y=10)
        self.setting_label_theme = ctk.CTkLabel(self.tab_setting, text="Theme:", text_color=["#262626 ", "white"], font=("Calibri", 15))
        self.setting_label_theme.place(x=10, y=10)

        # === Create tabview main ===
        self.tabview_main = ctk.CTkTabview(self, width=600, height=450)
        self.tabview_main.place(x=30, y=20)

        # --- Tabview main add ---
        self.tab_sort = self.tabview_main.add("SORTER")
        self.tab_dupe = self.tabview_main.add("DUPLICATED FINDER")

        #***SORT***
        self.sort_btn = CTkButton(self.tab_sort, text="Sort", text_color=["#262626","white"], corner_radius=8, fg_color=["#0c74ba","#343a40"], hover_color=["#0d344e","#0c74ba"], font=("Calibri", 15), command=self.sort_file)
        self.sort_btn.pack()
        self.sort_log_frame = CTkScrollableFrame(self.tab_sort, width=550, height=320, fg_color=["red", "#323333"])
        self.sort_log_frame.place(x=9, y=55)
        #***DUPE***
        self.sort_log_frame = CTkScrollableFrame(self.tab_dupe, width=550, height=320, fg_color=["red","#323333"])
        self.sort_log_frame.place(x=9, y=55)
        self.dupe_btn = CTkButton(self.tab_dupe, text="Find", text_color=["#262626", "white"], corner_radius=8, fg_color=["#0c74ba", "#343a40"], hover_color=["#0d344e", "#0c74ba"], font=("Calibri", 15), command=self.find_dupe)
        self.dupe_btn.pack()


# ====================  LOGIC UI ====================

    def select_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select folder")
        if self.folder_path:
            self.path_label.configure(text=f"CURRENT DIRECTORY ▶ {self.folder_path}")

    def sort_file(self):
        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select folder path before execute.")
            return

        messagebox_yon_1 = messagebox.askyesno(title="Do you want to proceed.", message="Press yes if you want to proceed.")
        if messagebox_yon_1:
            for filename in os.listdir(self.folder_path):
                self.file_path = os.path.join(self.folder_path, filename)

                if os.path.isfile(self.file_path):
                    self.ext = os.path.splitext(filename)[1].lower()

                    if filename.lower() == "desktop.ini":
                        continue

                    for folder, extension in self.logic.file_types.items():
                        if self.ext in extension:
                            target_dir = os.path.join(self.folder_path, folder)
                            os.makedirs(target_dir, exist_ok=True)
                            shutil.move(self.file_path, target_dir)
                            break

    def find_dupe(self):
        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select folder path before execute.")
            return

        self.hash_dict = defaultdict(list)
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                self.file_path = os.path.join(root, file)

                try:
                    self.file_hash = self.logic.get_file_hash(self.file_path)
                    self.hash_dict[self.file_hash].append(self.file_path)
                except Exception as e:
                    print(f"Error reading {self.file_path}: {e}")

        duplicate = {}
        for h, path in self.hash_dict.items():
            if len(path) > 1:
                duplicate[h] = path

        if duplicate:
            msg = self.curr+"\n"
            for h, path in duplicate.items():
                msg += f"Hash: {h}\n"
                for p in path:
                    msg += f"Path: {p}\n"

            messagebox_alert = messagebox.showinfo(title="Alert", message=msg)

            if messagebox_alert:
                choosedelfiles = filedialog.askopenfilenames(title="Select one or multiple file(s)")
                for choosedelfile in choosedelfiles:
                    try:
                        os.remove(choosedelfile)
                    except Exception as e:
                        messagebox.showerror("Error: 102", f"Can't remove {choosedelfile}: {e}")
        else:
            messagebox.showinfo(title="No duplicate file(s) found.", message="Scan complete. No duplicate file(s) were found.")