import os
import shutil
import hashlib
import time
import customtkinter as ctk

from tkinter import filedialog, messagebox
from collections import defaultdict

class FileLogic:
    def __init__(self):
        """เตรียม object logic เอาไว้ใช้ใน UI"""

        # ==================== dictionary that show support extension ====================
        self.file_types = {
            "Image": ['.jpg', '.jpeg', '.png', '.gif'],
            "Sound": ['.mp3', '.wav'],
            "Videos": ['.mp4', '.mov', '.avi', '.webm'],
            "Docs": ['.txt', '.pdf']
        }

        self.note = ("   We're excited to announce a major update for our"
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

        self.values = ["Light", "Dark", "System"]

        self.folder_path = ""

        self.curr = time.time()
        self.curr = time.ctime(self.curr)

        pass

    def select_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select folder")
        return self.folder_path

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

                    for folder, extension in self.file_types.items():
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
                    self.file_hash = self.get_file_hash(self.file_path)
                    self.hash_dict[self.file_hash].append(self.file_path)
                except Exception as e:
                    print(f"Error reading {self.file_path}: {e}")

        duplicate = {}
        for h, path in self.hash_dict.items():
            if len(path) > 1:
                duplicate[h] = path

        if duplicate:
            msg = self.curr + "\n"
            for h, path in duplicate.items():
                msg += f"Hash: {h}\n"
                for p in path:
                    msg += f"Path: {p}\n"

            messagebox_alert = messagebox.showinfo(title="Alert", message=msg)

            if messagebox_alert:
                choose_del_files = filedialog.askopenfilenames(title="Select one or multiple file(s)")
                for choose_del_file in choose_del_files:
                    try:
                        os.remove(choose_del_file)
                    except Exception as e:
                        messagebox.showerror("Error: 102", f"Can't remove {choose_del_file}: {e}")
        else:
            messagebox.showinfo(title="No duplicate file(s) found.",
                                message="Scan complete. No duplicate file(s) were found.")

    def get_file_hash(self, path, block_size=65536):
        self.hasher = hashlib.md5()
        with open(path, 'rb') as f:
            self.buf = f.read(block_size)
            while self.buf:
                self.hasher.update(self.buf)
                self.buf = f.read(block_size)
        return self.hasher.hexdigest()

    def theme(self, choice):

        if choice in self.values:
            ctk.set_appearance_mode(choice)
