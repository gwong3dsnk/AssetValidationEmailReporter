import os
import tkinter
from tkinter import *
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys, email_report, generate_graph_data, helper

BG_COLOR = "#444444"
LIGHT_GRAY_COLOR = "#eeeeee"


class ReporterUI:
    def __init__(self):
        # Use TkinterDnD.Tk() to allow for drag and drop functionality onto widgets
        self.csv_file_path_list = []
        self.csv_file_path = ""
        self.plot_file_path = ""
        self.graph_paths_per_csv = []
        self.working_dir = ""

        self.root_ui = TkinterDnD.Tk()
        self.root_ui.title("Asset Validation Email Reporter")
        self.root_ui.minsize(width=500, height=500)
        self.root_ui.config(padx=20, pady=20, bg=BG_COLOR)

        # Set up the menu bar
        menu_bar = Menu(self.root_ui)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open File(s)", command=self.do_nothing)
        file_menu.add_command(label="Open Folder", command=self.do_nothing)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Settings", command=self.open_settings_window)
        self.log_window_check_state = IntVar()
        edit_menu.add_checkbutton(
            label="Show Output Log",
            variable=self.log_window_check_state,
            command=self.toggle_log_window_visibility
        )
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.do_nothing)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root_ui.config(menu=menu_bar)

        # Set up the overall GUI
        title_label = Label(
            text="Asset Validation Email Reporter",
            font=("Arial", 18, "bold"),
            bg=BG_COLOR,
            fg="#bcbcbc",
        )
        title_label.grid(column=0, row=0, columnspan=7)

        summary_label = Label(
            text="This tool allows you to read in asset validation data_old in CSV format, generate visual graphs, "
                 "and send an email report to specified recipients.",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            wraplength=500,
            justify=LEFT
        )
        summary_label.grid(column=0, row=1, columnspan=7)

        ttk.Separator(self.root_ui, orient=HORIZONTAL).grid(
            column=0,
            row=2,
            columnspan=7,
            sticky="we",
            pady=10
        )

        date_combobox_label = Label(text="Select Data Date:", bg=BG_COLOR, fg=LIGHT_GRAY_COLOR)
        date_combobox_label.grid(column=0, row=3, sticky="w")

        self.date_folders = self.obtain_date_folders()
        self.selected_date = tkinter.StringVar()
        self.date_folder_combobox = ttk.Combobox(
            values=self.date_folders,
            state="readonly",
            textvariable=self.selected_date
        )
        self.date_folder_combobox.current(0)
        self.date_folder_combobox.grid(column=1, row=3)
        self.date_folder_combobox.bind("<<ComboboxSelected>>", self.date_folder_changed)

        ttk.Separator(self.root_ui, orient=VERTICAL).grid(
            column=2,
            row=3,
            sticky="nsw",
            padx=5
        )

        self.new_preset_name_entry = Entry()
        self.new_preset_name_entry.grid(column=3, row=3)

        self.save_new_preset_button = Button(text="Save Preset")
        self.save_new_preset_button.grid(column=4, row=3, padx=5)

        load_preset_combobox = ttk.Combobox()
        load_preset_combobox.grid(column=5, row=3)

        self.delete_preset_button = Button(text="Delete Preset")
        self.delete_preset_button.grid(column=6, row=3, padx=5)

        abs_path_label = Label(text="Folder Path:", bg=BG_COLOR, fg=LIGHT_GRAY_COLOR)
        abs_path_label.grid(column=0, row=4, sticky="w")

        self.abs_path_display_label = Label(text="Path Displayed Here", bg=BG_COLOR, fg="#b6d7a8")
        self.abs_path_display_label.grid(column=1, row=4, columnspan=5, sticky="w")

        csv_listbox_label = Label(
            text="STEP 1: Drag and drop 1 or more CSV files into the listbox below or select a date from the "
                 "dropdown menu above to load in all existing files for that date.",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            wraplength=500
        )
        csv_listbox_label.grid(column=0, row=5, columnspan=7)

        # Add a frame.  Establish scrollbar and listbox in frame.
        file_listbox_frame = Frame(self.root_ui)
        file_listbox_scrollbar = Scrollbar(file_listbox_frame, orient=HORIZONTAL)

        # Use drop_target_register to allow this widget to receive drag-and-drop files.
        # Bind to event <<Drop>> and specify the function to execute.
        self.csv_listbox = Listbox(
            file_listbox_frame,
            height=4,
            width=60,
            selectmode=MULTIPLE,
            xscrollcommand=file_listbox_scrollbar.set
        )
        file_listbox_scrollbar.config(command=self.csv_listbox.xview)
        file_listbox_scrollbar.pack(side=BOTTOM, fill=X)
        file_listbox_frame.grid(column=0, row=6, columnspan=7, pady=10)
        self.csv_listbox.pack()
        self.csv_listbox.drop_target_register(DND_FILES)
        self.csv_listbox.dnd_bind("<<Drop>>", self.drop_inside_csv_listbox)

        self.preview_graph_button = Button(text="Preview Graph(s)", command=self.send_csv_to_generate_data,
                                           state=DISABLED)
        self.preview_graph_button.grid(column=0, row=7, columnspan=5)

        self.clear_csv_listbox_button = Button(text="Clear CSV Listbox", command=self.clear_csv_listbox, state=DISABLED)
        self.clear_csv_listbox_button.grid(column=2, row=7, columnspan=7)

        email_addresses_listbox_label = Label(
            text="STEP 2: Add email addresses to the ADDRESS BOOK.  Then add the intended recipients "
                 "addresses to the RECIPIENTS",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            wraplength=500,
            justify=LEFT
        )
        email_addresses_listbox_label.grid(column=0, row=8, columnspan=7, pady=10)

        # Set up a frame to contain the email address widgets
        email_widgets_frame = Frame(self.root_ui, bg=BG_COLOR)
        email_widgets_frame.grid(column=0, row=9, columnspan=7)

        address_book_label = Label(
            email_widgets_frame,
            text="Address Book",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            font=("Arial", 10, "bold"),
        )
        address_book_label.grid(column=0, row=0)

        recipients_label = Label(
            email_widgets_frame,
            text="Recipient(s)",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            font=("Arial", 10, "bold"),
        )
        recipients_label.grid(column=2, row=0)

        self.address_book_listbox = Listbox(email_widgets_frame, height=4, width=35, selectmode=MULTIPLE)
        self.address_book_listbox.grid(column=0, row=1, rowspan=2, padx=10)

        self.recipient_address_listbox = Listbox(email_widgets_frame, height=4, width=35, selectmode=MULTIPLE)
        self.recipient_address_listbox.grid(column=2, row=1, rowspan=2, padx=10)

        self.add_recipient_button = Button(email_widgets_frame, text=">")
        self.add_recipient_button.grid(column=1, row=1)

        self.remove_recipient_button = Button(email_widgets_frame, text="<")
        self.remove_recipient_button.grid(column=1, row=2)

        self.add_new_email_address_entry = Entry(email_widgets_frame, width=35)
        self.add_new_email_address_entry.insert(0, "Type Email and hit Enter to ADD to Book")
        self.add_new_email_address_entry.grid(column=0, row=3, sticky="ns", pady=10)

        self.clear_recipient_listbox_button = Button(email_widgets_frame, text="Clear Recipients")
        self.clear_recipient_listbox_button.grid(column=2, row=3)

        send_email_report_label = Label(
            text="STEP 3: Send your email report to all recipients by clicking the button below.",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=LEFT
        )
        send_email_report_label.grid(column=0, row=10, columnspan=7)

        self.send_email_report_button = Button(text="Send Email Report", bg="green", command=self.send_email_report)
        self.send_email_report_button.grid(column=0, row=11, columnspan=7, pady=10)

        self.end_separator = ttk.Separator(self.root_ui, orient=HORIZONTAL)
        self.end_separator.grid_forget()

        self.log_window = ScrolledText(height=10, width=10)
        self.log_window.grid_forget()

        self.root_ui.mainloop()

    def do_nothing(self):
        pass

    def exit_app(self):
        sys.exit()

    def obtain_date_folders(self):
        """
        Get all the date folder names into a list and return it to populate the combobox GUI widget.
        :return date_folder_names: (list) folder names
        """
        date_folder_names = []
        self.working_dir = helper.get_working_dir_path()
        helper.directory_exists(self.working_dir)
        dir_items = os.listdir(self.working_dir)
        if len(dir_items) > 0:
            for item in dir_items:
                item_path = os.path.join(self.working_dir, item)
                if os.path.isdir(item_path):
                    date_folder_names.append(item)
                else:
                    print(f"{item} is a file.  It will not be added to the date combobox.")
        else:
            print(f"No date folders found at directory: {self.working_dir}")
        date_folder_names.insert(0, "-- Select Date --")

        return date_folder_names

    def date_folder_changed(self, event):
        # Clear the csv listbox of all contents
        self.clear_csv_listbox()
        self.csv_file_path_list = []

        selected_item_name = self.selected_date.get()
        if selected_item_name == "-- Select Date --":
            selected_item_path = "Path Displayed Here"
            print(f"No valid date selected from combobox.  Do nothing.")
        else:
            # Get contents from the date directory selected from the date combobox
            selected_item_path = os.path.join(self.working_dir, selected_item_name)
            selected_item_contents = os.listdir(selected_item_path)
            # Verify that csv files exist in directory
            if len(selected_item_contents) == 0:
                print(f"No CSV files found in: {selected_item_path}")
            else:
                for item in selected_item_contents:
                    file_path = os.path.join(selected_item_path, item)
                    if os.path.isfile(file_path) and file_path.endswith(".csv"):
                        file_path_clean = file_path.replace("\\", "/")
                        self.csv_listbox.insert(END, item)
                        self.csv_file_path_list.append(file_path_clean)
                self.preview_graph_button.config(state=ACTIVE)
                self.clear_csv_listbox_button.config(state=ACTIVE)

        self.abs_path_display_label.config(text=selected_item_path)

    def toggle_log_window_visibility(self):
        """
        Menu > Edit > Show Output Log
        Makes the output log visible or invisible based on menu check state
        :return: None
        """
        if self.log_window_check_state.get():
            self.end_separator.grid(column=0, row=13, columnspan=3, sticky="we", pady=10)
            self.log_window.grid(column=0, row=14, columnspan=3, sticky="nsew")
        else:
            self.end_separator.grid_forget()
            self.log_window.grid_forget()

    def parse_dropped_files(self, filename):
        """
        This function handles situations where file paths in the filename string contain spaces and surround the
        file path string with { }.  It cleans the file names, appends them to a new list and returns the list.
        Example filename:
            "{C:/Users/Owner/Desktop/Python Study/first csv.csv} C:/Users/Owner/Desktop/PythonStudy/second_csv.csv"
        :param filename: (str) String representation of paths for all files dragged and dropped into listbox
        :return clean_path_list: (list) List of all paths from files that were dragged and dropped into listbox
        """
        size = len(filename)
        clean_path_list = []
        name = ""
        idx = 0

        while idx < size:
            if filename[idx] == "{":  # Search the characters until you hit the first {
                j = idx + 1  # Get the first character of the file path
                while filename[j] != "}":
                    name += filename[j]  # The name var grows as it adds each character until it hits the }
                    j += 1
                clean_path_list.append(name)  # The full file path name gets appended to the list
                name = ""
                idx = j
            elif filename[idx] == " " and name != "":
                # If { not found, but space found, and name has been growing, append name to list
                clean_path_list.append(name)
                name = ""
            elif filename[idx] != " ":
                # If { not found and space not found, keep growing name string.
                name += filename[idx]
            idx += 1
        if name != "":  # Append the very last file path in the filename string to the list
            clean_path_list.append(name)

        return clean_path_list

    def drop_inside_csv_listbox(self, event):
        """
        Event called when a file drag-and-drop action is detected on the csv file listbox.
        Sends the string from event.data to be parsed and adds the cleaned file paths, on return, to the listbox
        :param event:TkinterDnD.DndEvent object
        :return: None
        """
        # The event variable is a string representation of the drag-and-dropped file paths.  File path str in data_old.
        self.csv_file_path_list = self.parse_dropped_files(event.data)

        for path in self.csv_file_path_list:
            if path.endswith(".csv"):
                self.csv_listbox.insert(END, path)
            else:
                print(f"{path} is not a csv file and will not be imported.")
                continue

        if self.csv_listbox.index(END) == 0:
            print("No valid CSV files found to add.")
        else:
            print("Valid CSV files found.")
            self.preview_graph_button.config(state=ACTIVE)
            self.clear_csv_listbox_button.config(state=ACTIVE)

    def clear_csv_listbox(self):
        """
        Clears the csv file listbox and disables the related buttons
        :return: None
        """
        self.csv_listbox.delete(0, END)
        self.preview_graph_button.config(state=DISABLED)
        self.clear_csv_listbox_button.config(state=DISABLED)
        self.abs_path_display_label.config(text="Path Displayed Here")

    def send_csv_to_generate_data(self):
        """
        For each csv file dragged into the widget, send the full path to parse through the data and generate the
        data reports.
        :return: None
        """
        self.obtain_date_folders()
        ggd = generate_graph_data.GenerateGraphData()

        for path in self.csv_file_path_list:
            self.csv_file_path = path
            self.graph_paths_per_csv = ggd.generate_reports(path)

    def send_email_report(self):
        """
        For each graph directory, send the full path to EmailReport() to generate the email
        body and send the email.
        :return:
        """
        for csv_paths_list in self.graph_paths_per_csv:
            er = email_report.EmailReport(csv_paths_list, self.csv_file_path)
            er.setup_email_properties()
            email = er.create_email_body()
            er.finalize_send_email(email)

    def open_settings_window(self):
        """
        Create new GUI window to house all Settings controls under the Edit menu bar item.
        :return:
        """
        settings_root_ui = tkinter.Tk()
        settings_root_ui.title("Settings")
        settings_root_ui.minsize(width=250, height=200)
        settings_root_ui.config(padx=20, pady=20, bg=BG_COLOR)

        email_title = Label(
            settings_root_ui,
            text="Email Settings",
            font=("Arial", 18, "bold"),
            bg=BG_COLOR,
            fg="#bcbcbc",
        )
        email_title.grid(column=0, row=0)

        sender_email_address_label = Label(
            settings_root_ui,
            text="Sender Email Address:",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=LEFT
        )
        sender_email_address_label.grid(column=0, row=1)

        sender_email_address_entry = Entry(settings_root_ui)
        sender_email_address_entry.grid(column=1, row=1)

        sender_email_password_label = Label(
            settings_root_ui,
            text="Sender Email Password:",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=LEFT
        )
        sender_email_password_label.grid(column=0, row=2)

        sender_email_password_entry = Entry(settings_root_ui)
        sender_email_password_entry.grid(column=1, row=2)

        smtp_server_address_label = Label(
            settings_root_ui,
            text="SMTP Server Address:",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=LEFT
        )
        smtp_server_address_label.grid(column=0, row=3)

        smtp_server_address_entry = Entry(settings_root_ui)
        smtp_server_address_entry.grid(column=1, row=3)

        smtp_server_port_label = Label(
            settings_root_ui,
            text="SMTP Server Port:",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=LEFT
        )
        smtp_server_port_label.grid(column=0, row=4)

        smtp_server_port_entry = Entry(settings_root_ui)
        smtp_server_port_entry.grid(column=1, row=4)

        email_info_button = Button(settings_root_ui, text="Save Information", command=self.save_email_information)
        email_info_button.grid(column=0, row=5, columnspan=2)

        settings_root_ui.mainloop()

    def save_email_information(self):
        """
        Save entered email information to json file - email_properties.json.
        NOTE: This is just for this test.  In reality I would save the information to env. variables.
        :return:
        """
        print("This button functionality has yet to be written.")
        pass
