import math
import os
import re
import shutil
import sys

from customtkinter import filedialog
import jsonpickle

import customtkinter as tk
from CTkMessagebox import CTkMessagebox
from datetime import date, datetime
from Archive import *
from PIL import Image
import threading


#  todo:
#           - from last time(8.3):
#               - finish the unloader - add an info to any unload
#               - add the ability to add a photo
#               - add an icon to a label to show on the unloader
#           - allow one window of each kind simultaneously
#           - add the ability to add info to labels
#           - creat backups!!

def return_default_stdout():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

def copy_files(src, dest):
    """
    copy all the files from the src directory to the dest directory in the background thread
    with using the windows copy function
    :param src: the source directory
    :param dest: the destination directory
    :return:
    """

    create_empty_folder(dest)
    for file in os.listdir(src):
        if os.path.isfile(src + "/" + file):
            shutil.copy2(src + "/" + file, dest)



    # for file in os.listdir(src):
    #     if os.path.isfile(src + "/" + file):
    #         shutil.copy2(src + "/" + file, dest)


def copy_files_thread(src, dest):
    """
    copy all the files from the src directory to the dest directory in the background thread
    with using the windows copy function
    :param src: the source directory
    :param dest: the destination directory
    :return:
    """
    thread = threading.Thread(target=copy_files, args=(src, dest))
    thread.start()


def create_empty_folder(folder_path):
    os.mkdir(folder_path)
    # open the new folder
    os.startfile(folder_path)

def dir_contains_dir(dir_path):
    for item in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, item)):
            return True
    return False

class MultiArchiveGUI:
    def __init__(self):

        self.chosen_labels_buttons = {}
        self.favorite_labels_buttons = {}
        self.searched_labels_buttons = {}
        self.archive = None
        self.load_archive()
        tk.set_appearance_mode("dark")
        tk.set_default_color_theme("blue")

        self.open_manager()
        self.row_nums = []
        self.row_values = []
        self.labels = []

        self.temp_item = {"name": "", "date": "", "dest_path": "", "src_path": "", "name_of_charge": "", "labels": [],
                          "free_text": "",
                          "thumbnail_user_path": "", "palga": "", "operation": "", "pikud": ""}
        self.in_middle_of_unloading = False

        # ------ for labels ------
        self.chosen_labels = []
        self.config_unloading_window_1()
        self.config_unloading_window_2()
        self.config_unloading_window_3()

    def load_archive(self):
        try:
            with open(ARCHIVE_DATA_PATH, 'r') as file:
                self.archive = jsonpickle.decode(json.load(file))
                self.logs_file =  open(ARCHIVE_ERROR_DATA_PATH, 'a', encoding='utf-8') 

                # Redirect stdout to the file
                sys.stdout = self.logs_file
                # Redirect stderr to stdout
                sys.stderr = self.logs_file
                print("\n\n")
                print("start of run ", datetime.now())


        except FileNotFoundError:
            # todo: show warning message, import from backups first before creating a new archive
            self.archive = Archive()
            self.save_archive()

        self.save_archive()

    def save_archive(self, file_name=ARCHIVE_DATA_PATH):
        with open(file_name, 'w') as file:
            json.dump(jsonpickle.encode(self.archive), file, indent=4)

    def open_manager(self):
        self.manager_window = tk.CTk()
        self.manager_window.geometry("1050x950")
        self.manager_window.title("Multi Archive")
        self.manager_window.grid_columnconfigure(0, weight=1)

        self.manager_window.grid_rowconfigure(4, weight=1)

        self.filtered_items = self.archive.items

        self.first_frame = tk.CTkFrame(self.manager_window, border_width=0)
        self.first_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
        self.first_frame.grid_columnconfigure(0, weight=1)
        self.first_frame.grid_columnconfigure(1, weight=1)
        self.first_frame.grid_rowconfigure(0, weight=1)

        self.search_unloading_button = ArchiveButton(self.first_frame, text="חפש פריקה", command=self.show_search_frame)
        self.search_unloading_button.grid(row=0, column=0, pady=5, padx=10, sticky="nsew", columnspan=1)

        self.new_unloading_button = ArchiveButton(self.first_frame, text="פריקה חדשה", command=self.open_new_unloading)
        self.new_unloading_button.grid(row=0, column=1, pady=5, padx=10, sticky="nsew", columnspan=1)

        # ------------------------------------ first frame - search by ------------------------------------
        self.search_frame = tk.CTkFrame(self.manager_window, border_width=2)
        # self.search_frame.grid(row=1, column=0, pady=(10, 0), padx=20, sticky="nsew")

        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_by_name_label = tk.CTkLabel(self.search_frame, text="שם", font=("Arial", 15))
        self.search_by_name_label.grid(row=0, column=5, pady=5, padx=10)

        self.search_by_name_entry = tk.CTkEntry(self.search_frame, width=ENTRY_WIDTH, font=("Arial", 15))
        self.search_by_name_entry.grid(row=0, column=4, pady=5, padx=10)

        self.search_by_date_label = tk.CTkLabel(self.search_frame, text="תאריך", font=("Arial", 15))
        self.search_by_date_label.grid(row=0, column=3, pady=5, padx=10)

        self.search_by_date_after_entry = tk.CTkEntry(self.search_frame, width=ENTRY_WIDTH, font=("Arial", 15),
                                                      placeholder_text="נפרק מתאריך")
        self.search_by_date_after_entry.grid(row=0, column=2, pady=5, padx=10)

        self.search_by_date_before_entry = tk.CTkEntry(self.search_frame, width=ENTRY_WIDTH, font=("Arial", 15),
                                                       placeholder_text="נפרק לפני תאריך")
        self.search_by_date_before_entry.grid(row=0, column=1, pady=5, padx=10)

        # self.search_by_labels_label = tk.CTkLabel(self.search_frame, text="תוויות", font=("Arial", 15))
        # self.search_by_labels_label.grid(row=2, column=0, pady=5, padx=10, columnspan=5, sticky="ew")
        #
        self.search_by_labels_frame = tk.CTkFrame(self.search_frame, height=10)
        self.search_by_labels_frame.grid_columnconfigure(0, weight=1)
        self.search_by_labels_frame.grid_columnconfigure(1, weight=1)
        self.search_by_labels_frame.grid_columnconfigure(2, weight=1)
        self.search_by_labels_frame.grid_columnconfigure(3, weight=1)
        self.search_by_labels_frame.grid_columnconfigure(4, weight=1)
        self.search_by_labels_frame.grid_rowconfigure(0, weight=0)
        self.search_by_labels_frame.grid(row=3, column=0, pady=5, padx=0, columnspan=5, sticky="nsew")
        self.search_labels_frame_manager = tk.CTkFrame(self.search_frame, height=50, width=1, border_width=2)

        self.chosen_labels_frame_manager = ArchiveLabelsFrame(self.search_by_labels_frame, self,
                                                              self.search_labels_frame_manager)
        self.chosen_labels_frame_manager.grid(row=0, column=0, pady=5, padx=10, columnspan=5, sticky="nsew")


        self.advanced_search_button = tk.CTkButton(self.search_frame, text="חיפוש מתקדם",
                                                   command=self.advanced_search_by,
                                                   font=("Arial", 15))
        self.advanced_search_button.grid(row=1, column=0, pady=5, padx=10, columnspan=1)

        # ------------------------------------ advanced search frame ------------------------------------

        self.advanced_search_frame = tk.CTkFrame(self.manager_window, border_width=2)
        self.advanced_search_frame.columnconfigure(0, weight=1)

        self.search_by_name_of_charge_label = tk.CTkLabel(self.advanced_search_frame, text="שם הפורק",
                                                          font=("Arial", 15))
        self.search_by_name_of_charge_label.grid(row=0, column=3, pady=5, padx=0)

        self.search_by_name_of_charge_entry = tk.CTkEntry(self.advanced_search_frame, width=ENTRY_WIDTH,
                                                          font=("Arial", 15))
        self.search_by_name_of_charge_entry.grid(row=0, column=2, pady=5, padx=0)

        self.search_by_name_of_pikud_label = tk.CTkLabel(self.advanced_search_frame, text="שם הפיקוד",
                                                         font=("Arial", 15))
        self.search_by_name_of_pikud_label.grid(row=0, column=1, pady=5, padx=0)

        self.search_by_name_of_pikud_entry = ArchiveComboBox(self.advanced_search_frame,
                                                             values=self.archive.get_pikuds())

        self.search_by_name_of_pikud_entry.grid(row=0, column=0, pady=5, padx=0)

        self.search_by_name_of_palga_label = tk.CTkLabel(self.advanced_search_frame, text="שם הפלגה",
                                                         font=("Arial", 15))
        self.search_by_name_of_palga_label.grid(row=1, column=3, pady=5, padx=10)

        self.search_by_name_of_palga_entry = ArchiveComboBox(self.advanced_search_frame,
                                                             values=self.archive.get_palgot())

        self.search_by_name_of_palga_entry.grid(row=1, column=2, pady=5, padx=0)

        self.search_by_name_of_operation_label = tk.CTkLabel(self.advanced_search_frame, text="שם המבצע",
                                                             font=("Arial", 15))
        self.search_by_name_of_operation_label.grid(row=1, column=1, pady=5, padx=10)

        self.search_by_name_of_operation_entry = ArchiveComboBox(self.advanced_search_frame,
                                                                 values=self.archive.get_operations())

        self.search_by_name_of_operation_entry.grid(row=1, column=0, pady=5, padx=10)

        self.search_by_free_text_label = tk.CTkLabel(self.advanced_search_frame, text="טקסט חופשי", font=("Arial", 15))
        self.search_by_free_text_label.grid(row=2, column=3, pady=5, padx=10)

        self.search_by_free_text_entry = tk.CTkEntry(self.advanced_search_frame, width=ENTRY_WIDTH * 3,
                                                     font=("Arial", 15))
        self.search_by_free_text_entry.grid(row=2, column=0, pady=5, padx=0, columnspan=3)

        self.search_by_button = tk.CTkButton(self.manager_window, text="חפש", command=self.search_by,
                                             font=("Arial", 15))
        # self.search_by_button.grid(row=3, column=0, pady=5, padx=10, columnspan=1)

        # ------------------------------------ unloading frame ------------------------------------
        self.unloading_frame = tk.CTkFrame(self.manager_window, border_width=2)
        self.unloading_frame.grid(row=4, column=0, pady=20, padx=20, sticky="nsew")
        self.unloading_frame.grid_columnconfigure(0, weight=1)
        self.unloading_frame.grid_rowconfigure(0, weight=1)

        self.scrollbar = tk.CTkScrollableFrame(self.unloading_frame, height=700)
        self.scrollbar.grid_columnconfigure(0, weight=1)

        self.scrollbar.grid(row=0, column=0, pady=5, padx=10, sticky="nsew")
        self.show_unloadings()


    def open_new_unloading(self):
        # checks if there is already a window open
        if self.in_middle_of_unloading:
            # show a warning message
            msg = ArchiveWarning(title="שגיאה", message="כבר קיים חלון פריקה חדשה.\n הפריקה החדשה תימחק")
            response = msg.get()
            if response != msg.continue_anyway_message:
                return
            else:
                self.reconfigure_unloading_windows()
                # print("המשיך")

        self.in_middle_of_unloading = True
        self.returned = False
        # self.config_unloading_window_1()
        self.new_unloading_window_1.deiconify()



    def done(self):  # transfer the unloading to the archive

        # optional: show the user a view of the new item
        """
        create a new item and add it to the archive
        transfer the unloading to the archive

        :return:
        """
        dest_path = os.path.join(self.temp_item["dest_path"], self.temp_item["dir_name"])
        self.archive.add_new_item(name=self.temp_item["name"],
                                  date=self.temp_item["date"],
                                  dest_path=dest_path,
                                  name_of_charge=self.temp_item["name_of_charge"],
                                  labels={label.name: label for label in self.temp_item["labels"]},
                                  free_text=self.temp_item["free_text"],
                                  thumbnail_path=self.temp_item["thumbnail_user_path"],
                                  palga=self.temp_item["palga"],
                                  operation=self.temp_item["operation"],
                                  pikud=self.temp_item["pikud"])


        self.save_archive()
        # refresh the manager
        self.reconfigure_unloadings_frame()

    def select_src_directory(self):
        src_dir = filedialog.askdirectory()
        self.src_entry.configure(state="normal")
        self.src_entry.delete(0, "end")
        self.src_entry.insert(0, src_dir)
        self.src_entry.configure(state="disabled")

    def select_dest_directory(self):
        dest_dir = filedialog.askdirectory()
        self.dest_entry.configure(state="normal")
        self.dest_entry.delete(0, "end")
        self.dest_entry.insert(0, dest_dir)
        self.dest_entry.configure(state="disabled")



    def run(self):
        self.manager_window.mainloop()
        self.save_archive(os.path.join(BACKUPS_PATH, self.archive.backup_update()))
        self.save_archive()


        # print(self.archive.__str__())
        # print(self.archive.get_items_dic())
        self.archive.make_data()
        self.save_archive()

        print("end of run ", datetime.now())
        print("_______________________________________________________________________")
        self.logs_file.close()
        return_default_stdout()

    def show_unloadings(self):
        counter = self.filtered_items.__len__()
        showed_items = []

        for item in self.filtered_items:
            counter = counter - 1
            item_frame = ItemFrame(self.scrollbar, item, ItemDetailsWindow, self.archive)
            item_frame.grid(row=int(counter), pady=5, padx=5, column=0, sticky="ew")
            showed_items.append(item_frame)

    def show_item(self, item):  # shows all the item details when points on item
        message_box = CTkMessagebox(title="פרטי הפריקה", message=item.__dic__(), font=("Arial", 15),
                                    icon="info", option_1="סגור")
        response = message_box.get()

        pass

    def open_folder(self, item):
        os.startfile(item.dest_path)

    def filter_by(self):
        pass

    def sort_by(self):
        pass

    def search_by(self):
        self.search_frame.grid_forget()
        self.search_by_button.grid_forget()
        self.advanced_search_frame.grid_forget()
        self.filtered_items = self.archive.Items_filtered_by(self.search_by_name_entry.get(),
                                                             self.search_by_date_after_entry.get(),
                                                             self.search_by_date_before_entry.get(),
                                                             self.search_by_name_of_charge_entry.get(),
                                                             self.chosen_labels_frame_manager.get_chosen_labels(),
                                                             self.search_by_name_of_pikud_entry.get(),
                                                             self.search_by_name_of_operation_entry.get(),
                                                             self.search_by_name_of_palga_entry.get(),

                                                             self.search_by_free_text_entry.get())

        self.reconfigure_unloadings_frame()

        pass

    def advanced_search_by(self):
        self.show_advanced_search_frame()
        pass

    def show_search_frame(self):
        self.search_frame.grid(row=1, column=0, padx=20, sticky="nsew")
        self.search_by_button.grid(row=3, column=0, pady=5, padx=10, columnspan=1)

    def show_advanced_search_frame(self):
        self.advanced_search_frame.grid(row=2, column=0, padx=20, sticky="nsew")

    def remove_item(self, item):
        self.archive.remove_item(item)
        self.save_archive()
        self.manager_window.destroy()
        self.open_manager()

    def update_temp_item(self, current_stage):
        if current_stage == 1:
            self.temp_item["name"] = self.unload_name_entry.get()
            self.temp_item["date"] = self.unload_date_entry.get()
            self.temp_item["name_of_charge"] = self.unloader_name_entry.get()
            self.temp_item["src_path"] = self.src_entry.get()
            self.temp_item["dest_path"] = self.dest_entry.get()

        elif current_stage == 2:
            self.temp_item["labels"] = self.chosen_labels_frame_unload.get_chosen_labels()
            self.temp_item["thumbnail_user_path"] = self.thumbnail_path_entry.get()

        elif current_stage == 3:

            self.temp_item["free_text"] = self.info_entry.get()
            self.temp_item["palga"] = self.unload_palga_entry.get()
            self.temp_item["operation"] = self.unload_operation_entry.get()
            self.temp_item["pikud"] = self.unload_pikud_entry.get()

    def next_stage(self, current_stage):
        self.update_temp_item(current_stage)
        self.validate_unloading_details(current_stage)

    def validate_unloading_details(self,
                                   current_stage):  # check if all the details are valid, save them and exit the window
        if current_stage == 1:
            if not is_valid_file_name(self.temp_item["name"]):
                self.show_error("שם הפריקה אינו תקין")
                return
            if not is_valid_date(self.temp_item["date"]):
                self.show_error("תאריך הפריקה אינו תקין")
                return
            if not is_valid_file_name(self.temp_item["name_of_charge"]):
                self.show_error("שם הפורק אינו תקין")
                return

            if not is_valid_path(self.temp_item["src_path"]):
                if not self.temp_item["src_path"]:
                    response = ArchiveWarning(title="אזהרה", message="לא נבחרה תיקיית מקור \n תיווצר פריקה ריקה").get()
                    if response == "Cancel":
                        return
                    elif response == "המשך בכל זאת":
                        self.temp_item["src_path"] = ""
                else:
                    self.show_error("נתיב המקור אינו תקין")
                    return

            if not is_valid_path(self.temp_item["dest_path"]):
                self.show_error("נתיב היעד אינו תקין")
                return
            self.new_unloading_window_1.withdraw()
            self.move_to_stage(2)

        elif current_stage == 2:
            if not self.temp_item["labels"]:
                response = ArchiveWarning(title="אזהרה", message="לא נבחרו תוויות").get()
                if response == "Cancel":
                    return
                elif response == "המשך בכל זאת":
                    self.temp_item["labels"] = []

            if not is_valid_path(self.temp_item["thumbnail_user_path"]):
                if not self.temp_item["thumbnail_user_path"]:
                    response = ArchiveWarning(title="אזהרה",
                                              message="לא נבחרה תמונת תצוגה \n תיווצר תמונת תצוגה ריקה").get()
                    if response == "Cancel":
                        return
                    elif response == "המשך בכל זאת":
                        self.temp_item["thumbnail_user_path"] = DEFAULT_THUMBNAIL_PATH

                else:
                    self.show_error("נתיב התמונה אינו תקין")
                    return
            self.new_unloading_window_2.withdraw()
            self.move_to_stage(3)



        elif current_stage == 3:
            try:

                self.new_unloading_window_3.withdraw()
                self.temp_item["dir_name"] = str(self.temp_item["date"]) + \
                                             " - " + self.temp_item["name"] + \
                                             " - " + str(self.archive.get_next_free_id())
                dest_path = os.path.join(self.temp_item["dest_path"], self.temp_item["dir_name"])

                if self.temp_item["src_path"]:
                    # copy the files from the source to the destination in the background
                    if dir_contains_dir(self.temp_item["src_path"]):
                        self.show_error("שימו לב כי יש תיקיות בתיקיית המקור שלא יועברו")
                    copy_files_thread(self.temp_item["src_path"], dest_path)

                else:
                    # create a new empty folder
                    create_empty_folder(dest_path)
            except OSError as e:
                print(e)
                self.show_error("שגיאה ביצירת תיקיית היעד")
                return

            self.done()
            self.in_middle_of_unloading = False
            self.reconfigure_unloading_windows()
            # self.manager_window.destroy()
            # self.open_manager()

    def exit_unloading(self):

        msg = ArchiveWarning(title="שגיאה", message="הפריקה החדשה תימחק")
        response = msg.get()
        if response != msg.continue_anyway_message:
            return
        else:
            self.in_middle_of_unloading = False
            self.reconfigure_unloading_windows()
            # print("המשיך")


        pass

    def destroy_unloading_windows(self):
        self.new_unloading_window_1.destroy()
        self.new_unloading_window_2.destroy()
        self.new_unloading_window_3.destroy()

    def config_unloading_window_1(self):
        self.new_unloading_window_1 = ArchiveTopLevelWindow(self.manager_window, self.archive, "פריקה חדשה")
        self.new_unloading_window_1.rowconfigure(0, weight=-0)
        # ------------------------------------ first frame ------------------------------------
        first_frame = tk.CTkFrame(self.new_unloading_window_1)
        first_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        first_frame.grid_columnconfigure(0, weight=1)
        first_frame.grid_columnconfigure(1, weight=1)

        define_unload_label = ArchiveLabel(first_frame, "הגדר פריקה")
        define_unload_label.grid(row=0, column=1, pady=5, padx=10, sticky="e")

        stage_unload_label = ArchiveLabel(first_frame, "שלב 1 מתוך 3")
        stage_unload_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        # ------------------------------------ second frame ------------------------------------
        second_frame = tk.CTkFrame(self.new_unloading_window_1, border_width=2)
        second_frame.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")

        second_frame.grid_columnconfigure(0, weight=1)
        second_frame.grid_columnconfigure(1, weight=1)
        second_frame.grid_columnconfigure(2, weight=1)

        unload_name_label = ArchiveLabel(second_frame, text="שם הפריקה")
        unload_name_label.grid(row=0, column=2, pady=5, padx=10)

        self.unload_name_entry = ArchiveEntry(second_frame)
        self.unload_name_entry.grid(row=1, column=2, pady=5, padx=10, sticky="ew")

        unload_date_label = ArchiveLabel(second_frame, text="תאריך הפריקה")
        unload_date_label.grid(row=0, column=1, pady=5, padx=10)
        self.unload_date_entry = tk.CTkEntry(second_frame, width=ENTRY_WIDTH, font=("Arial", 15))
        self.unload_date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.unload_date_entry.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

        unloader_name_label = ArchiveLabel(second_frame, text="שם הפורק")
        unloader_name_label.grid(row=0, column=0, pady=5, padx=10)
        self.unloader_name_entry = ArchiveEntry(second_frame)
        self.unloader_name_entry.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        # ------------------------------------ third frame ------------------------------------
        third_frame = tk.CTkFrame(self.new_unloading_window_1, border_width=2, width=ENTRY_WIDTH * 4 + 20)
        third_frame.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")
        third_frame.grid_columnconfigure(0, weight=1)
        third_frame.grid_columnconfigure(1, weight=1)

        self.source_label = ArchiveLabel(third_frame, text="מקור הפריקה")
        self.source_label.grid(row=0, column=2, pady=5, padx=10, sticky="e")
        self.src_entry = tk.CTkEntry(third_frame, font=("Arial", 15))
        self.src_entry.grid(row=0, column=0, pady=5, padx=10, columnspan=2, sticky="ew")
        self.src_entry.configure(state="disabled")
        src_button = ArchiveButton(third_frame, text="בחר תיקיית מקור", command=self.select_src_directory)
        src_button.grid(row=1, column=0, pady=5, padx=10, sticky="nsew", columnspan=3)

        self.dest_label = ArchiveLabel(third_frame, text="יעד הפריקה")
        self.dest_label.grid(row=2, column=2, pady=5, padx=10)
        self.dest_entry = ArchiveEntry(third_frame)
        self.dest_entry.grid(row=2, column=0, pady=5, padx=10, columnspan=2, sticky="ew")
        self.dest_entry.configure(state="disabled")
        dest_button = ArchiveButton(third_frame, text="בחר תיקיית יעד", command=self.select_dest_directory)
        dest_button.grid(row=3, column=0, pady=5, padx=10, sticky="nsew", columnspan=3)


        # ------------------------------------ forth frame ------------------------------------
        forth_frame = tk.CTkFrame(self.new_unloading_window_1, border_width=2)
        forth_frame.grid(row=3, column=0, pady=20, padx=20, sticky="nsew")

        forth_frame.grid_columnconfigure(0, weight=1)

        self.next_button = ArchiveButton(forth_frame, text="הבא", command=lambda: self.next_stage(1))
        self.next_button.grid(row=0, column=0, pady=5, padx=10, sticky="ns")

        self.new_unloading_window_1.withdraw()
        self.new_unloading_window_1.protocol("WM_DELETE_WINDOW", self.exit_unloading)

    def config_unloading_window_2(self):
        self.new_unloading_window_2 = ArchiveTopLevelWindow(self.manager_window, self.archive, "פריקה חדשה",
                                                            geometry="650x800")
        self.new_unloading_window_2.rowconfigure(0, weight=-0)
        # ------------------------------------ first frame ------------------------------------
        first_frame = tk.CTkFrame(self.new_unloading_window_2)
        first_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        first_frame.grid_columnconfigure(0, weight=1)
        first_frame.grid_columnconfigure(1, weight=1)

        define_unload_label = ArchiveLabel(first_frame, "אפיין פריקה")
        define_unload_label.grid(row=0, column=1, pady=5, padx=10, sticky="e")

        stage_unload_label = ArchiveLabel(first_frame, "שלב 2 מתוך 3")
        stage_unload_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        # ------------------------------------ second frame ------------------------------------
        self.searched_labels_buttons = {}
        self.chosen_labels_buttons = {}
        self.chosen_labels = []
        self.favorite_labels_buttons = {}

        second_frame = tk.CTkFrame(self.new_unloading_window_2, border_width=2)
        second_frame.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")

        second_frame.grid_columnconfigure(0, weight=1)
        second_frame.grid_columnconfigure(1, weight=1)
        second_frame.grid_columnconfigure(2, weight=1)
        second_frame.grid_columnconfigure(3, weight=1)
        second_frame.grid_columnconfigure(4, weight=1)
        second_frame.grid_columnconfigure(5, weight=1)

        # labels_label = ArchiveLabel(second_frame, text="תוויות")
        # labels_label.grid(row=0, column=0, pady=5, padx=10, sticky="ns", columnspan=6)
        self.search_labels_frame_unload = tk.CTkFrame(second_frame, border_width=0, height=60)

        self.chosen_labels_frame_unload = ArchiveLabelsFrame(second_frame, self, self.search_labels_frame_unload)
        # tk.CTkFrame(second_frame, border_width=2, height=60)
        self.chosen_labels_frame_unload.grid(row=1, column=0, pady=5, padx=10, sticky="ew", columnspan=6)


        # ------------------------------------ image frame ------------------------------------
        self.image_frame = tk.CTkFrame(self.new_unloading_window_2, border_width=2)
        self.image_frame.grid(row=3, column=0, pady=20, padx=20, sticky="nsew")

        self.image_frame.grid_columnconfigure(0, weight=1)

        self.image_label = ArchiveLabel(self.image_frame, text="תמונה")
        self.image_label.grid(row=0, column=0, pady=5, padx=10, sticky="ns")

        self.thumbnail_button = ArchiveButton(self.image_frame, text="בחר תמונה", command=self.select_image)
        self.thumbnail_button.grid(row=1, column=0, pady=5, padx=10, sticky="ns")

        self.thumbnail_path_entry = ArchiveEntry(self.image_frame)
        self.thumbnail_path_entry.configure(state="disabled")
        self.thumbnail_path_entry.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

        # ------------------------------------ forth frame ------------------------------------

        self.new_unloading_window_2.rowconfigure(4, weight=1)

        forth_frame = tk.CTkFrame(self.new_unloading_window_2, border_width=2)
        forth_frame.grid(row=4, column=0, pady=20, padx=20, sticky="nsew")

        forth_frame.grid_columnconfigure(0, weight=1)
        forth_frame.grid_rowconfigure(0, weight=1)

        self.next_button = ArchiveButton(forth_frame, text="הבא", command=lambda: self.next_stage(2))
        self.next_button.grid(row=0, column=0, pady=5, padx=10, sticky="w")
        self.return_button = ArchiveButton(forth_frame, text="חזור", command=lambda: self.return_stage(2))
        self.return_button.grid(row=0, column=1, pady=5, padx=10, sticky="e")

        self.new_unloading_window_2.withdraw()
        self.new_unloading_window_2.protocol("WM_DELETE_WINDOW", self.exit_unloading)


    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=IMAGE_TYPES)
        if self.image_path:
            self.thumbnail_button.configure(text="החלף תמונה")
            fill_path_entry(self.thumbnail_path_entry, self.image_path)

            self.chosen_image = Image.open(self.image_path)
            self.chosen_image = self.chosen_image.resize(THUMBNAILS_SIZE)
            self.chosen_image = tk.CTkImage(light_image=self.chosen_image, dark_image=self.chosen_image,
                                            size=(192, 108))
            self.image_label = tk.CTkLabel(self.image_frame, image=self.chosen_image, text="")
            self.image_label.grid(row=3, column=0, pady=5, padx=10, sticky="ew")


    def config_unloading_window_3(self):
        self.new_unloading_window_3 = ArchiveTopLevelWindow(self.manager_window, self.archive, "פריקה חדשה")
        self.new_unloading_window_3.rowconfigure(0, weight=0)
        # ------------------------------------ first frame ------------------------------------
        first_frame = tk.CTkFrame(self.new_unloading_window_3)
        first_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        first_frame.grid_columnconfigure(0, weight=1)
        first_frame.grid_columnconfigure(1, weight=1)

        define_unload_label = ArchiveLabel(first_frame, "אפיין פריקה")
        define_unload_label.grid(row=0, column=1, pady=5, padx=10, sticky="e")

        stage_unload_label = ArchiveLabel(first_frame, "שלב 3 מתוך 3")
        stage_unload_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        # ------------------------------------ second frame ------------------------------------
        second_frame = tk.CTkFrame(self.new_unloading_window_3, border_width=2)
        second_frame.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")

        second_frame.grid_columnconfigure(0, weight=1)
        second_frame.grid_columnconfigure(1, weight=1)
        second_frame.grid_columnconfigure(2, weight=1)

        self.unload_palga_label = ArchiveLabel(second_frame, text="פלגה")
        self.unload_palga_label.grid(row=0, column=2, pady=5, padx=10)

        self.unload_palga_entry = ArchiveComboBox(second_frame, values=self.archive.get_palgot())
        self.unload_palga_entry.grid(row=1, column=2, pady=5, padx=10, sticky="ew")

        unload_operation_label = ArchiveLabel(second_frame, text="מבצע")
        unload_operation_label.grid(row=0, column=1, pady=5, padx=10)

        self.unload_operation_entry = ArchiveComboBox(second_frame, values=self.archive.get_operations())
        self.unload_operation_entry.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

        unload_pikud_label = ArchiveLabel(second_frame, text="פיקוד")
        unload_pikud_label.grid(row=0, column=0, pady=5, padx=10)

        self.unload_pikud_entry = ArchiveComboBox(second_frame, values=self.archive.get_pikuds())
        self.unload_pikud_entry.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        # ------------------------------------ info frame ------------------------------------
        info_frame = tk.CTkFrame(self.new_unloading_window_3, border_width=2)
        info_frame.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")

        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)

        self.info_label = ArchiveLabel(info_frame, text="מידע נוסף")
        self.info_label.grid(row=0, column=0, pady=5, padx=10, sticky="ns", columnspan=2)

        self.info_entry = ArchiveEntry(info_frame)
        self.info_entry.grid(row=1, column=0, pady=5, padx=10, sticky="nsew", columnspan=2, rowspan=2)

        # ------------------------------------ forth frame ------------------------------------
        forth_frame = tk.CTkFrame(self.new_unloading_window_3, border_width=2)
        forth_frame.grid(row=4, column=0, pady=20, padx=20, sticky="nsew")

        forth_frame.grid_columnconfigure(0, weight=1)

        self.next_button = ArchiveButton(forth_frame, text="סיים", command=lambda: self.next_stage(3))
        self.next_button.grid(row=0, column=0, pady=5, padx=10, sticky="w")
        self.next_button = ArchiveButton(forth_frame, text="חזור", command=lambda: self.return_stage(3))
        self.next_button.grid(row=0, column=1, pady=5, padx=10, sticky="e")

        self.new_unloading_window_3.withdraw()
        self.new_unloading_window_3.protocol("WM_DELETE_WINDOW", self.exit_unloading)


    def return_stage(self, current_stage):
        self.returned = True
        if current_stage == 2:
            self.update_temp_item(2)
            self.new_unloading_window_2.withdraw()

            self.move_to_stage(1)
        elif current_stage == 3:
            self.update_temp_item(3)
            self.new_unloading_window_3.withdraw()

            self.move_to_stage(2)

    def fill_stage(self, current_stage):
        if not self.returned:
            return
        if current_stage == 1:
            self.unload_name_entry.insert(0, self.temp_item["name"])
            self.unload_date_entry.delete(0, "end")
            self.unload_date_entry.insert(0, self.temp_item["date"])
            self.unloader_name_entry.insert(0, self.temp_item["name_of_charge"])
            fill_path_entry(self.src_entry, self.temp_item["src_path"])
            fill_path_entry(self.dest_entry, self.temp_item["dest_path"])
        elif current_stage == 2:  # todo: support return

            pass

        elif current_stage == 3:
            self.info_entry.insert(0, self.temp_item["free_text"])
            self.unload_palga_entry.set(self.temp_item["palga"])
            self.unload_operation_entry.set(self.temp_item["operation"])
            self.unload_pikud_entry.set(self.temp_item["pikud"])



    def show_error(self, message):
        ArchiveError(title="שגיאה בפריקה", message=message)

    def move_to_stage(self, desired_stage):
        if desired_stage == 1:
            self.new_unloading_window_1.deiconify()
        elif desired_stage == 2:
            self.new_unloading_window_2.deiconify()

        elif desired_stage == 3:
            self.new_unloading_window_3.deiconify()


    def reconfigure_unloadings_frame(self):
        self.unloading_frame.destroy()
        self.unloading_frame = tk.CTkFrame(self.manager_window, border_width=2)
        self.unloading_frame.grid(row=4, column=0, pady=20, padx=20, sticky="nsew")
        self.unloading_frame.grid_columnconfigure(0, weight=1)
        self.unloading_frame.grid_rowconfigure(0, weight=1)
        self.scrollbar.destroy()
        self.scrollbar = tk.CTkScrollableFrame(self.unloading_frame, height=700)
        self.scrollbar.grid(row=0, column=0, pady=5, padx=10, sticky="nsew")
        self.scrollbar.grid_columnconfigure(0, weight=1)
        self.show_unloadings()

    def reconfigure_unloading_windows(self):
        self.new_unloading_window_1.destroy()
        self.new_unloading_window_2.destroy()
        self.new_unloading_window_3.destroy()
        self.config_unloading_window_1()
        self.config_unloading_window_2()
        self.config_unloading_window_3()


def list_to_string(my_list):
    return str(my_list).replace("[", "").replace("]", "").replace("'", "")


class ItemDetailsWindow(tk.CTkToplevel):
    def __init__(self, master, item, archive):
        super().__init__(master)
        self.geometry("550x470")
        self.title("פרטי הפריקה")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.item = item
        self.archive = archive
        self.fill_window()

    def fill_window(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.details_frame = tk.CTkFrame(self)
        self.details_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(1, weight=1)

        pathToImage = self.item.thumbnail
        if not is_valid_path(pathToImage):
            pathToImage = DEFAULT_THUMBNAIL_PATH
        my_image = Image.open(pathToImage)
        image = tk.CTkImage(light_image=my_image, dark_image=my_image, size=(192, 108))
        self.item_thumbnail = tk.CTkLabel(self, image=image, text="")
        self.item_thumbnail.grid(row=0, column=1, pady=20, padx=10, sticky="new", rowspan=3)

        self.item_name_label = ArchiveLabel(self.details_frame, text=self.item.name)
        self.item_name_label.configure(font=("Arial", 25))
        self.item_name_label.grid(row=0, column=1, pady=5, padx=10, sticky="ew")

        self.item_date_label = ArchiveLabel(self.details_frame, text="נפרק בתאריך: " + self.item.date)
        self.item_date_label.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

        self.item_unloader_label = ArchiveLabel(self.details_frame, text="נפרק על ידי: " + self.item.name_of_charge)
        self.item_unloader_label.grid(row=2, column=1, pady=5, padx=10, sticky="ew")

        extra_details_text = self.get_item_extra_details()
        self.item_extra_details_label = ArchiveLabel(self.details_frame, text=extra_details_text)
        self.item_extra_details_label.grid(row=3, column=1, pady=5, padx=10, sticky="ew")

        self.item_labels_frame = tk.CTkFrame(self.details_frame)
        self.item_labels_frame.grid(row=4, column=1, pady=5, padx=10, sticky="ew")
        self.labels_buttons_dict = {}
        organize_labels(self.item_labels_frame, self.item.labels.values(), 0, 5, self.labels_buttons_dict)

        self.item_info_label = ArchiveLabel(self.details_frame, text="מידע נוסף: " + self.item.free_text)
        self.item_info_label.grid(row=5, column=1, pady=5, padx=10, sticky="ew")

        self.item_open_button = ArchiveButton(self, text="פתח תיקייה", command=self.open_folder)
        self.item_open_button.grid(row=1, column=0, pady=5, padx=10, sticky="ew", columnspan=2)


    def get_item_extra_details(self):
        extra_details_text = ""
        if self.item.palga != "":
            extra_details_text += " | " + self.item.palga + " | "
        if self.item.operation != "":
            extra_details_text += " | " + self.item.operation + " | "
        if self.item.pikud != "":
            extra_details_text += " | " + self.item.pikud + " | "

        return extra_details_text

    def open_folder(self):
        try:
            os.startfile(self.item.dest_path)
        except OSError as e:
            CTkMessagebox(title="שגיאה", message="לא ניתן לפתוח את התיקייה", icon="error", option_1="סגור")
            return
        self.item.open_item()
    def edit_item(self):
        pass


class ItemFrame(tk.CTkFrame):
    def __init__(self, master, item, edit_func, archive):
        super().__init__(master)

        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.item = item
        self.archive = archive

        pathToImage = item.thumbnail
        if not is_valid_path(pathToImage):
            pathToImage = DEFAULT_THUMBNAIL_PATH
        my_image = Image.open(pathToImage)
        image = tk.CTkImage(light_image=my_image, dark_image=my_image, size=(192, 108))
        self.item_image = tk.CTkLabel(self, image=image, text="")
        self.item_image.grid(row=0, column=3, pady=5, padx=10, sticky="ew")

        item_text = item.name + "\n" + item.date
        self.item_label = tk.CTkLabel(self, text=item_text, font=("Arial", 25))
        self.item_label.grid(row=0, column=2, pady=5, padx=10, sticky="ew")

        self.item_first_labels_frame = tk.CTkFrame(self, border_width=0, height=40)
        self.item_first_labels_frame.grid(row=1, column=2, pady=5, padx=10, sticky="ew")
        self.labels_buttons_dict = {}

        list_of_four_labels = list(item.labels.values())[:3]
        organize_labels(self.item_first_labels_frame, list_of_four_labels, 0, 4, self.labels_buttons_dict)

        self.item_details_button = tk.CTkButton(self, text="פרטים", command=lambda: edit_func(self, item, self.archive),
                                                font=("Arial", 15))
        self.item_details_button.grid(row=2, column=0, pady=5, padx=10, sticky="ew", columnspan=2)

        self.item_open_button = tk.CTkButton(self, text="פתח תיקייה", command=self.open_folder,
                                             font=("Arial", 15))
        self.item_open_button.grid(row=1, column=0, pady=5, padx=10, sticky="ew", columnspan=2)

        self.item_delete_button = ArchiveButton(self, text="מחק פריקה", command=self.remove_item)
        self.item_delete_button.configure(bg_color="red", height=30, width=30, font=("Arial", 10))
        self.item_delete_button.grid(row=0, column=0, pady=5, padx=10, sticky="wn", columnspan=1)
        # self.bind("<Enter>", command= self.show_item)

    def show_item(self, event):
        message_box = CTkMessagebox(title="פרטי הפריקה", message=self.item.__dic__(), font=("Arial", 15),
                                    icon="info", option_1="סגור")
        response = message_box.get()

    def open_folder(self):
        os.startfile(self.item.dest_path)

    def remove_item(self):
        delete_message = ArchiveWarning(title="מחיקת פריקה",
                                        message="הפעולה הבאה תמחק את תיעוד הפריקה, אך לא את תיקיית הפריקה")
        response = delete_message.get()
        if response == "המשך בכל זאת":
            self.archive.remove_item(self.item)
            self.destroy()


class ArchiveTopLevelWindow(tk.CTkToplevel):
    def __init__(self, master, archive, title, geometry="550x470"):
        super().__init__(master)
        self.archive = archive
        self.geometry(geometry)
        self.title(title)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


class ArchiveComboBox(tk.CTkComboBox):
    def __init__(self, master, values):
        super().__init__(master, values=values, font=(FONT, 15), dropdown_font=(FONT, 15), justify="right")

    def get(self):
        return super().get()


class ArchiveLabel(tk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(master, text=text, font=(FONT, 15), justify="right")


class ArchiveEntry(tk.CTkEntry):
    def __init__(self, master):
        super().__init__(master, font=(FONT, 15), justify="right")


class ArchiveButton(tk.CTkButton):
    def __init__(self, master, text, command):
        super().__init__(master, text=text, command=command, font=(FONT, 15))


class ArchiveLabelButton(tk.CTkButton):
    def __init__(self, master, text, command, label, command_func, coordinates=(0, 0)):
        if command_func is None:
            super().__init__(master, text=text, command=lambda: None,
                             font=(FONT, 12), width=50,
                             height=30, hover=True)
        else:
            super().__init__(master, text=text, command=lambda: command_func(label),
                             font=(FONT, 12), width=50,
                             height=30, hover=True)
        self.label = label
        self.coordinates = coordinates

    def getLabelName(self):
        return self.label.name


def organize_labels(frame, labels, row, col, buttons_dict, command_func=None, chosen_labels_buttons=None):
    labels_in_row = col

    for label in labels:
        col = col - 1
        if col < 0:
            col = labels_in_row - 1
            row = row + 1

        label_button = ArchiveLabelButton(frame, text=label.name,
                                          command=lambda: None,
                                          label=label, coordinates=(row, col), command_func=command_func)
        buttons_dict[label.name] = label_button
        if chosen_labels_buttons and not chosen_labels_buttons.get(label.name) or not chosen_labels_buttons:
            label_button.grid(row=row, column=col, pady=5, padx=10)


class ArchiveLabelsFrame(tk.CTkFrame):
    def __init__(self, master, archiveGUI, search_labels_frame, labels_in_row=LABELS_IN_ROW):
        super().__init__(master)
        self.chosen_labels = []
        self.labels_in_row = labels_in_row
        self.archiveGUI = archiveGUI
        self.chosen_labels_frame = tk.CTkFrame(self, border_width=2, height=60)
        self.favorite_labels_buttons = {}
        self.chosen_labels_buttons = {}
        self.searched_labels_buttons = {}
        self.show_more_labels_button_row = 3

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)

        self.labels_label = ArchiveLabel(self, text="תוויות")
        self.labels_label.grid(row=0, column=0, pady=5, padx=10, sticky="ns", columnspan=6)

        self.chosen_labels_frame.grid(row=1, column=0, pady=5, padx=10, sticky="ew", columnspan=6)
        self.grid_rowconfigure(1, weight=0)
        self.chosen_labels_frame.grid_columnconfigure(0, weight=1)
        self.chosen_labels_frame.grid_columnconfigure(1, weight=1)
        self.chosen_labels_frame.grid_columnconfigure(2, weight=1)
        self.chosen_labels_frame.grid_columnconfigure(3, weight=1)
        self.chosen_labels_frame.grid_columnconfigure(4, weight=1)
        self.chosen_labels_frame.grid_columnconfigure(5, weight=1)

        self.favorite_labels_label = ArchiveLabel(self, text=":תוויות נפוצות")
        self.favorite_labels_label.grid(row=2, column=labels_in_row, pady=5, padx=10, sticky="ns")

        self.fill_labels_frame_by_favorite(row=2, chosen_labels_frame=self.chosen_labels_frame)

        self.show_more_labels_button = ArchiveButton(self, text="הצג עוד תוויות",
                                                     command=lambda: self.show_more_labels(
                                                         last_row=self.show_more_labels_button_row))
        self.show_more_labels_button.grid(row=3, column=0, pady=5, padx=10, sticky="ns", columnspan=3)
        self.search_for_labels_button = ArchiveButton(self, text="חפש תוויות",
                                                      command=lambda: self.search_labels(
                                                          search_labels_frame=search_labels_frame,
                                                          chosen_labels_frame=self.chosen_labels_frame))
        self.search_for_labels_button.grid(row=3, column=3, pady=5, padx=10, sticky="ns", columnspan=3)

    def fill_labels_frame_by_favorite(self, row, chosen_labels_frame):
        labels = self.archiveGUI.archive.get_favorite_labels(start=self.favorite_labels_buttons.__len__(),
                                                             n=self.labels_in_row)
        col = labels.__len__()
        organize_labels(self, labels, row, col, self.favorite_labels_buttons, self.choose_label,
                        chosen_labels_buttons=self.chosen_labels_buttons)

    def show_more_labels(self, last_row):
        self.show_more_labels_button.grid_forget()
        self.search_for_labels_button.grid_forget()

        self.fill_labels_frame_by_favorite(row=self.show_more_labels_button_row,
                                           chosen_labels_frame=self.chosen_labels_frame)
        self.update_last_row()

        self.show_more_labels_button.grid(row=self.show_more_labels_button_row, column=0, pady=5, padx=10, sticky="ns",
                                          columnspan=3)
        self.search_for_labels_button.grid(row=self.show_more_labels_button_row, column=3, pady=5, padx=10, sticky="ns",
                                           columnspan=3)

    def search_labels(self, search_labels_frame, chosen_labels_frame):
        search_labels_frame.grid(row=4, column=0, pady=(0, 10), padx=10, sticky="nsew", columnspan=6)
        search_labels_frame.grid_columnconfigure(0, weight=1)
        search_labels_frame.grid_columnconfigure(1, weight=1)
        search_labels_frame.grid_columnconfigure(2, weight=1)
        search_labels_frame.grid_columnconfigure(3, weight=1)
        search_labels_frame.grid_columnconfigure(4, weight=1)
        search_labels_frame.grid_columnconfigure(5, weight=1)

        self.search_by_name_label = ArchiveLabel(search_labels_frame, text="שם התווית")
        self.search_by_name_label.grid(row=0, column=5, pady=5, padx=10, sticky="e")

        self.search_by_name_entry = ArchiveEntry(search_labels_frame)
        self.search_by_name_entry.grid(row=0, column=4, pady=5, padx=10, sticky="ew")

        self.search_by_name_button = ArchiveButton(search_labels_frame, text="חפש תווית",
                                                   command=lambda: self.show_labels_contains(
                                                       self.search_by_name_entry.get(),
                                                       chosen_labels_frame=chosen_labels_frame,
                                                       search_labels_frame=search_labels_frame))
        self.search_by_name_button.grid(row=0, column=3, pady=5, padx=10, sticky="ew")

        self.add_new_label_button = ArchiveButton(search_labels_frame, text="הוסף תווית חדשה",
                                                  command=lambda: self.add_new_label())
        self.add_new_label_button.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        pass

    def show_labels_contains(self, name, chosen_labels_frame, search_labels_frame):
        labels = self.archiveGUI.archive.get_labels_contains(name)  # todo: remove the GUI
        for name, button in self.searched_labels_buttons.items():
            button.grid_forget()

        self.searched_labels_buttons = {}
        organize_labels(search_labels_frame, labels, 1, self.labels_in_row, self.searched_labels_buttons,
                        self.choose_label, chosen_labels_buttons=self.chosen_labels_buttons)

    def get_chosen_labels(self):
        return self.chosen_labels

    def choose_label(self, label):
        row = math.floor(self.chosen_labels.__len__() / self.labels_in_row)
        col = self.chosen_labels.__len__() % self.labels_in_row
        self.chosen_labels.append(label)

        self.chosen_labels_buttons[label.name] = ArchiveLabelButton(self.chosen_labels_frame, text=label.name,
                                                                    command=lambda: self.unchoose_label(label),
                                                                    label=label,
                                                                    coordinates=(row, col),
                                                                    command_func=self.unchoose_label)
        self.chosen_labels_buttons[label.name].configure(command=lambda: self.unchoose_label(label))
        self.chosen_labels_buttons[label.name].grid(row=row, column=col,
                                                    pady=5, padx=10, sticky="ns")
        if self.favorite_labels_buttons.get(label.name):
            self.favorite_labels_buttons[label.name].grid_forget()
        if self.searched_labels_buttons.get(label.name):
            self.searched_labels_buttons[label.name].grid_forget()

    def unchoose_label(self, label):
        if self.favorite_labels_buttons.get(label.name):
            coordinates = self.favorite_labels_buttons[label.name].coordinates
            self.favorite_labels_buttons[label.name].grid(row=coordinates[0], column=coordinates[1],
                                                          pady=5, padx=10, sticky="ns")

        if self.searched_labels_buttons.get(label.name):
            coordinates = self.searched_labels_buttons[label.name].coordinates
            self.searched_labels_buttons[label.name].grid(row=coordinates[0], column=coordinates[1],
                                                          pady=5, padx=10, sticky="ns")

        self.chosen_labels_buttons[label.name].grid_forget()
        self.chosen_labels_buttons.pop(label.name)
        self.chosen_labels.remove(label)

    def add_new_label(self):
        dialog = tk.CTkInputDialog(text="שם התווית", title="הוסף תווית חדשה", font=("Arial", 15))
        name_of_new_label = dialog.get_input()
        try:
            new_label = self.archiveGUI.archive.add_label(name_of_new_label)  # todo: add info
        except ValueError as e:
            msg = CTkMessagebox(title="Error", message=str(e), font=("Arial", 15),
                                option_1="Cancel", option_2="נסה שוב")
            response = msg.get()
            if response == "נסה שוב":
                self.add_new_label()

            return

        self.choose_label(new_label)

    def update_last_row(self):
        self.show_more_labels_button_row = 2 + int(self.favorite_labels_buttons.__len__() / self.labels_in_row) + \
                                           1 * int(self.favorite_labels_buttons.__len__() % self.labels_in_row != 0)


class ArchiveError(CTkMessagebox):
    def __init__(self, title, message):
        super().__init__(title=title, message=message, font=(FONT, 15),
                         icon="cancel", option_1="OK")


class ArchiveWarning(CTkMessagebox):
    def __init__(self, title, message):
        super().__init__(title=title, message=message, font=(FONT, 15),
                         icon="warning", option_1="המשך בכל זאת", option_2="Cancel")
        self.continue_anyway_message = "המשך בכל זאת"



def validate_input(user_input, validity_function):
    return validity_function(user_input)


def is_valid_name(name):
    return name.__len__() > 0


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_valid_file_name(name):
    # remove spaces
    name = name.replace(" ", "")
    pattern = r'^[\w\-.]+$'
    return bool(re.match(pattern, name))


def is_valid_path(path):
    return os.path.exists(path)


def fill_path_entry(entry, path):
    entry.configure(state="normal")
    entry.delete(0, "end")
    entry.insert(0, path)
    entry.configure(state="disabled")
