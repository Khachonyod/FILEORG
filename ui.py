import customtkinter as ctk

from customtkinter import CTkButton, CTkLabel, set_appearance_mode, CTkScrollableFrame, CTkOptionMenu, CTkProgressBar
from logic import FileLogic


class FileORGApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("1000x600")
        self.resizable(0,0)
        set_appearance_mode("Dark")

        self.logic = FileLogic()

# ==================== UI ====================

        # ===SELECT FOLDER===
        self.select_folder_btn = CTkButton(
            self,
            text="SELECT FOLDER",
            text_color=("white", "white"),
            corner_radius=8,
            fg_color=("#0c74ba", "#343a40"),
            hover_color=("#0d344e", "#0c74ba"),
            font=("Calibri",15),
            command=self.select_folder
        )
        self.select_folder_btn.place(x=10, y=560)
        # ===PATH LABEL===
        self.path_label = CTkLabel(
            self,
            text="PLEASE SELECT FOLDER FIRST",
            text_color=("#262626", "white"),
            corner_radius=8,
            fg_color=("#999999", "#6c757d"),
            font=("Calibri",15)
        )
        self.path_label.place(x=155, y=560)

        # === Create tabview setting ===
        self.tabview_setting = ctk.CTkTabview(self, width=300, height=550)
        self.tabview_setting.place(x=670, y=20)

        self.tab_whatnew = self.tabview_setting.add("What's New")
        self.tab_setting = self.tabview_setting.add("Setting")
        self.tab_about = self.tabview_setting.add("About")

        #***WHAT"S NEW***
        self.patch_note = CTkLabel(
            self.tab_whatnew,
            text=self.logic.note,
            text_color=("#262626", "white"),
            justify="left",
            font=("Calibri",12)
        )
        self.patch_note.place(x=0, y=95)

        self.nameapp = CTkLabel(
            self.tab_whatnew,
            text="FileORG",
            text_color=("#262626", "white"),
            font=("Impact", 40)
        )
        self.nameapp.place(x=81,y=5)

        self.ver_label = CTkLabel(
            self.tab_whatnew,
            text="2.0.0-alpha",
            text_color=("#262626", "white"),
            font=("Calibri", 18)
        )
        self.ver_label.place(x=0, y=65)

        # ***SETTING***
        self.setting_opt_theme = CTkOptionMenu(
            self.tab_setting,
            values=self.logic.values,
            command=self.logic.theme,
            button_color=("#6c757d", "#0c74ba"),
            button_hover_color=("#595959", "#4297e4"),
            fg_color=("black", "#6c757d"),
            dropdown_hover_color="#0c74ba"
        )
        self.setting_opt_theme.set("Dark")
        self.setting_opt_theme.place(x=75,y=10)

        self.setting_label_theme = ctk.CTkLabel(
            self.tab_setting,
            text="Theme:",
            text_color=("#262626", "white"),
            font=("Calibri", 15)
        )
        self.setting_label_theme.place(x=10, y=10)

        # ***ABOUT***
        self.about_label = CTkLabel(self.tab_about, text="Made by JWU")
        self.about_label.place(x=100, y=5)

        # === Create tabview main ===
        self.tabview_main = ctk.CTkTabview(self, width=600, height=450)
        self.tabview_main.place(x=30, y=20)

        self.tab_sort = self.tabview_main.add("SORTER")
        self.tab_dupe = self.tabview_main.add("DUPLICATED FINDER")

        #***SORT***
        self.sort_btn = CTkButton(
            self.tab_sort,
            text="Sort",
            text_color=("white", "white"),
            corner_radius=8,
            fg_color=("#0c74ba", "#343a40"),
            hover_color=("#0d344e", "#0c74ba"),
            font=("Calibri", 15),
            command=self.logic.sort_file
        )
        self.sort_btn.pack()

        self.sort_log_frame = CTkScrollableFrame(
            self.tab_sort,
            width=550,
            height=320,
            fg_color=("white", "#323333")
        )
        self.sort_log_frame.place(x=9, y=55)

        #***DUPE***
        self.dupe_log_frame = CTkScrollableFrame(
            self.tab_dupe,
            width=550,
            height=320,
            fg_color=("white", "#323333")
        )
        self.dupe_log_frame.place(x=9, y=55)

        self.dupe_btn = CTkButton(
            self.tab_dupe,
            text="Find",
            text_color=("white", "white"),
            corner_radius=8,
            fg_color=("#0c74ba", "#343a40"),
            hover_color=("#0d344e", "#0c74ba"),
            font=("Calibri", 15),
            command=self.logic.find_dupe
        )
        self.dupe_btn.pack()


    def select_folder(self):
        folder = self.logic.select_folder()
        if folder:
            self.path_label.configure(text=f"CURRENT DIRECTORY ▶ {folder}")