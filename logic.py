import os
import shutil
import hashlib
import customtkinter as ctk


class FileLogic:
    def __init__(self):
        """เตรียม object logic เอาไว้ใช้ใน UI"""
        # === dictionary that show support extension ===
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

        pass

    def get_file_hash(self, path, block_size=65536):
        self.hasher = hashlib.md5()
        with open(path, 'rb') as f:
            self.buf = f.read(block_size)
            while self.buf:
                self.hasher.update(self.buf)
                self.buf = f.read(block_size)
        return self.hasher.hexdigest()

    def theme(self, choice):
        if choice == "Light":
            ctk.set_appearance_mode("Light")
        elif choice == "Dark":
            ctk.set_appearance_mode("Dark")
        elif choice == "System":
            ctk.set_appearance_mode("System")