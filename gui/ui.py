import os, json, subprocess
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
        self.csv_file_path_list = []
        self.csv_file_path = ""
        self.plot_file_path = ""
        self.graph_paths_per_csv = []
        self.working_dir, self.proj_data_dir = helper.get_working_dir_path()
        self.full_line_report = []

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

        # GUI widgets for date folder selection
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

        # GUI widgets for Preset controls
        self.new_preset_name_entry = Entry()
        self.new_preset_name_entry.grid(column=3, row=3)

        self.save_new_preset_button = Button(text="Save Preset", command=self.save_new_preset)
        self.save_new_preset_button.grid(column=4, row=3, padx=5)

        self.preset_names = self.get_existing_presets()
        self.selected_preset = tkinter.StringVar()
        self.load_preset_combobox = ttk.Combobox(
            values=self.preset_names,
            state="readonly",
            textvariable=self.selected_preset
        )
        self.load_preset_combobox.current(0)
        self.load_preset_combobox.grid(column=5, row=3)
        self.load_preset_combobox.bind("<<ComboboxSelected>>", self.load_existing_presets)

        self.delete_preset_button = Button(text="Delete Preset", command=self.delete_selected_preset)
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

        # Add a frame to attach h and v scrollbars to the csv list widget.
        file_listbox_frame = Frame(self.root_ui)
        file_listbox_frame.grid(column=0, row=6, columnspan=7, pady=10)
        file_listbox_h_scrollbar = Scrollbar(file_listbox_frame, orient=HORIZONTAL)
        file_listbox_v_scrollbar = Scrollbar(file_listbox_frame, orient=VERTICAL)

        # Use drop_target_register to allow this widget to receive drag-and-drop files.
        # Bind to event <<Drop>> and specify the function to execute.
        self.csv_listbox = Listbox(
            file_listbox_frame,
            height=4,
            width=60,
            selectmode=MULTIPLE,
            xscrollcommand=file_listbox_h_scrollbar.set,
            yscrollcommand=file_listbox_v_scrollbar.set
        )
        file_listbox_h_scrollbar.config(command=self.csv_listbox.xview)
        file_listbox_h_scrollbar.pack(side=BOTTOM, fill=X)
        file_listbox_v_scrollbar.config(command=self.csv_listbox.yview)
        file_listbox_v_scrollbar.pack(side=RIGHT, fill=Y)

        self.csv_listbox.pack()
        self.csv_listbox.drop_target_register(DND_FILES)
        self.csv_listbox.dnd_bind("<<Drop>>", self.drop_inside_csv_listbox)

        self.preview_graph_button = Button(text="Preview Graph(s)", command=self.send_csv_to_generate_data)
        self.preview_graph_button.grid(column=0, row=7, columnspan=5)

        self.clear_csv_listbox_button = Button(text="Clear CSV Listbox", command=self.clear_csv_listbox)
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

        # Set up a nested frame to attach v and h scrollbars to the address book list widget
        address_book_listbox_frame = Frame(email_widgets_frame)
        address_book_listbox_frame.grid(column=0, row=1, rowspan=2, padx=10)

        address_book_h_scrollbar = Scrollbar(address_book_listbox_frame, orient=HORIZONTAL)
        address_book_v_scrollbar = Scrollbar(address_book_listbox_frame, orient=VERTICAL)

        self.address_book_listbox = Listbox(
            address_book_listbox_frame,
            height=4,
            width=35,
            selectmode=MULTIPLE,
            xscrollcommand=address_book_h_scrollbar.set,
            yscrollcommand=address_book_v_scrollbar.set
        )
        self.load_address_book()
        self.address_book_listbox.bind("<Delete>", self.remove_from_address_book)
        self.address_book_listbox.bind("<BackSpace>", self.remove_from_address_book)

        address_book_h_scrollbar.config(command=self.address_book_listbox.xview)
        address_book_h_scrollbar.pack(side=BOTTOM, fill=X)
        address_book_v_scrollbar.config(command=self.address_book_listbox.yview)
        address_book_v_scrollbar.pack(side=RIGHT, fill=Y)
        self.address_book_listbox.pack()

        # Set up another nested frame to attach v and h scrollbars to the recipients list widget
        recipient_listbox_frame = Frame(email_widgets_frame)
        recipient_listbox_frame.grid(column=2, row=1, rowspan=2, padx=10)

        recipient_h_scrollbar = Scrollbar(recipient_listbox_frame, orient=HORIZONTAL)
        recipient_v_scrollbar = Scrollbar(recipient_listbox_frame, orient=VERTICAL)

        self.recipient_address_listbox = Listbox(
            recipient_listbox_frame,
            height=4,
            width=35,
            selectmode=MULTIPLE,
            xscrollcommand=recipient_h_scrollbar.set,
            yscrollcommand=recipient_v_scrollbar.set
        )

        recipient_h_scrollbar.config(command=self.recipient_address_listbox.xview)
        recipient_h_scrollbar.pack(side=BOTTOM, fill=X)
        recipient_v_scrollbar.config(command=self.recipient_address_listbox.yview)
        recipient_v_scrollbar.pack(side=RIGHT, fill=Y)
        self.recipient_address_listbox.pack()

        # < > buttons to add/remove email addresses from the book to the recipient list widget
        self.add_recipient_button = Button(email_widgets_frame, text=">", command=self.add_recipient_email)
        self.add_recipient_button.grid(column=1, row=1)
        self.remove_recipient_button = Button(email_widgets_frame, text="<", command=self.remove_recipient_email)
        self.remove_recipient_button.grid(column=1, row=2)

        self.add_new_email_address_entry = Entry(email_widgets_frame, width=35)
        self.add_new_email_address_entry.insert(0, "Type Email and hit Enter to ADD to Book")
        self.add_new_email_address_entry.grid(column=0, row=3, sticky="ns", pady=10)
        self.add_new_email_address_entry.bind("<Return>", self.add_email_to_book)
        self.add_new_email_address_entry.bind("<Button-1>", self.address_entry_on_click)

        self.clear_recipient_listbox_button = Button(email_widgets_frame, text="Clear Recipients",
                                                     command=self.clear_recipient_listbox)
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

    def delete_selected_preset(self):
        current_selected_preset = self.load_preset_combobox.get()
        with open(f"{self.proj_data_dir}/presets.json", "r") as f:
            contents = json.load(f)
            for data in contents:
                if data["preset_name"] == current_selected_preset:
                    idx = contents.index(data)
                    del contents[idx]
        open(f"{self.proj_data_dir}/presets.json", "w").close()
        with open(f"{self.proj_data_dir}/presets.json", "r+") as f:
            json.dump(contents, f, indent=4)

        self.clear_csv_listbox()
        self.recipient_address_listbox.delete(0, END)

    def get_existing_presets(self):
        """
        Read the previously saved presets from the presets.json, get the preset names, refresh the preset combobox
        :return:
        """
        preset_names = []
        with open(f"{self.proj_data_dir}/presets.json", "r") as f:
            contents = json.load(f)
            for data in contents:
                preset_names.append(data["preset_name"])

        return preset_names

    def load_existing_presets(self, event):
        """
        Executed when the user selects an option from the preset dropdown menu that isn't the index 0 option.
        Loads the preset data into the GUI elements where data is found.
        :param event: ComboboxSelected binding
        :return: None
        """
        selected_preset = self.load_preset_combobox.get()

        with open(f"{self.proj_data_dir}/presets.json", "r") as f:
            contents = json.load(f)
            self.csv_file_path_list = []
            for preset_dict in contents:
                if preset_dict["preset_name"] == selected_preset:
                    self.date_folder_combobox.set(preset_dict["date_folder"])
                    self.abs_path_display_label.config(text=preset_dict["date_folder_path"])
                    self.recipient_address_listbox.delete(0, END)
                    for address in preset_dict["recipient_addresses"]:
                        self.recipient_address_listbox.insert(END, address)
                    self.csv_listbox.delete(0, END)
                    for csv_path in preset_dict["csv_files"]:
                        self.csv_file_path_list.append(csv_path)
                        csv_display_path, file_path_clean = helper.change_to_relative_path(csv_path)
                        self.csv_listbox.insert(END, csv_display_path)

    def save_new_preset(self):
        """
        Requires Preset name to be entered in GUI as well as email addresses in the recipient listbox to save
        properly.  Date folder choice and csv files are optional.
        :return:
        """
        recipient_contents = self.recipient_address_listbox.get(0, END)
        preset_name = self.new_preset_name_entry.get()
        date_folder_name = self.date_folder_combobox.get()
        date_abs_path = self.abs_path_display_label.cget("text").replace("\\", "/")

        if preset_name != "" and recipient_contents:
            new_preset_dict = {
                "preset_name": preset_name,
                "date_folder": date_folder_name,
                "date_folder_path": date_abs_path,
                "recipient_addresses": recipient_contents,
                "csv_files": self.csv_file_path_list
            }

            with open(f"{self.proj_data_dir}/presets.json", "r+") as f:
                content = json.load(f)
                existing_content = content
            open(f"{self.proj_data_dir}/presets.json", "w").close()
            with open(f"{self.proj_data_dir}/presets.json", "r+") as f:
                existing_content.append(new_preset_dict)
                json.dump(existing_content, f, indent=4)
                f.write("\n")

            self.new_preset_name_entry.delete(0, END)

            # Repopulate values in the preset combo box
            self.preset_names = self.get_existing_presets()
            self.load_preset_combobox.delete(0, END)
            self.load_preset_combobox.config(values=self.preset_names)
            newly_created_preset = self.preset_names[len(self.preset_names) - 1]
            self.load_preset_combobox.set(newly_created_preset)

        else:
            print("Failed to save new preset.  Check to make sure you have entered a new preset name in the textfield,"
                  "and that you have added email addresses to the recipient listbox.")

    def remove_from_address_book(self, event):
        """
        Delete an email address from the address book list widget and from the address book txt file when user has
        emails in the list widget selected.
        :param event: User presses the Backspace or Delete keys
        :return:
        """
        current_selection = self.address_book_listbox.curselection()
        n = len(current_selection) - 1
        while n >= 0:
            cur_item_text = self.address_book_listbox.get(n)
            self.address_book_listbox.delete(current_selection[n])

            with open(f"{self.proj_data_dir}/address_book.txt", "r") as f:
                lines = f.readlines()
            with open(f"{self.proj_data_dir}/address_book.txt", "w") as f:
                for line in lines:
                    if line != cur_item_text:
                        f.write(line)
            n -= 1

    def add_recipient_email(self):
        """
        Get a tuple of indices from which get the corresponding string and strip out the newline.  Then add the
        email address to the recipient list widget.
        :return:
        """
        selected_emails = self.address_book_listbox.curselection()
        for email in selected_emails:
            address = self.address_book_listbox.get(email).strip()
            existing_recipients = self.recipient_address_listbox.get(0, END)
            if address not in existing_recipients:
                self.recipient_address_listbox.insert(END, address)

    def remove_recipient_email(self):
        """
        Get a tuple of indices and using the len of this tuple as an index, remove the corresponding item from the
        recipient address listbox.
        :return:
        """
        selected_emails = self.recipient_address_listbox.curselection()
        n = len(selected_emails) - 1
        while n >= 0:
            self.recipient_address_listbox.delete(selected_emails[n])
            n -= 1

    def clear_recipient_listbox(self):
        self.recipient_address_listbox.delete(0, END)

    def load_address_book(self):
        """
        On app start, populate the address book listbox with the contents of the address book txt file.
        :return:
        """
        with open(f"{self.proj_data_dir}/address_book.txt", "r") as f:
            emails = f.readlines()
            emails.sort()
            if not emails:
                print("No existing emails found.  Please add new ones.")
            else:
                for address in emails:
                    self.address_book_listbox.insert(END, address)
        with open(f"{self.proj_data_dir}/address_book.txt", "w") as f:
            # Overwrite existing txt contents with sorted content.
            for line in emails:
                f.write(f"{line}")

    def add_email_to_book(self, event):
        """
        If the new email doesn't already exist in the address book txt file, add it to the txt file, sort, then
        refresh the address book list widget contents.
        :param event:
        :return:
        """
        current_entry_text = self.add_new_email_address_entry.get()
        # There is very likely a better way to validate the string as a proper email address, but for now this'll do.
        if "@" and "." in current_entry_text:
            self.address_book_listbox.insert(END, current_entry_text)
            self.add_new_email_address_entry.delete(0, END)

            with open(f"{self.proj_data_dir}/address_book.txt", "r") as f:
                lines = f.readlines()
                if f"{current_entry_text}\n" not in lines:
                    lines.append(f"{current_entry_text}\n")
                lines.sort()  # Sort txt file contents alphabetically

            self.address_book_listbox.delete(0, END)

            with open(f"{self.proj_data_dir}/address_book.txt", "w") as f:
                # Overwrite existing txt contents with sorted content.
                for line in lines:
                    f.write(f"{line}")
                    self.address_book_listbox.insert(END, line)

    def address_entry_on_click(self, event):
        self.add_new_email_address_entry.delete(0, END)

    def obtain_date_folders(self):
        """
        Get all the date folder names into a list and return it to populate the combobox GUI widget.
        :return date_folder_names: (list) folder names
        """
        date_folder_names = []
        dir_items = os.listdir(self.working_dir)
        if len(dir_items) > 0:
            for item in dir_items:
                item_path = os.path.join(self.working_dir, item)
                if os.path.isdir(item_path):
                    date_folder_names.append(item)
        else:
            print(f"No date folders found at directory: {self.working_dir}")
        date_folder_names.insert(0, "-- Select Date --")

        return date_folder_names

    def date_folder_changed(self, event):
        # Clear the csv listbox of all contents
        self.csv_listbox.delete(0, END)
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
                        relative_path, file_path_clean = helper.change_to_relative_path(file_path)
                        self.csv_listbox.insert(END, relative_path)
                        self.csv_file_path_list.append(file_path_clean)

        self.abs_path_display_label.config(text=selected_item_path)

    def toggle_log_window_visibility(self):
        """
        Menu > Edit > Show Output Log
        Makes the output log visible or invisible based on menu check state
        :return: None
        """
        if self.log_window_check_state.get():
            self.end_separator.grid(column=0, row=13, columnspan=7, sticky="we", pady=10)
            self.log_window.grid(column=0, row=14, columnspan=7, sticky="nsew")
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
        # Reset date combobox and absolute path
        self.date_folder_combobox.set("-- Select Date --")
        self.csv_listbox.delete(0, END)
        self.abs_path_display_label.config(text="Path Displayed Here")

        # The event variable is a string representation of the drag-and-dropped file paths.  File path str in data_old.
        self.csv_file_path_list = self.parse_dropped_files(event.data)

        for path in self.csv_file_path_list:
            if path.endswith(".csv"):
                relative_path, file_path_clean = helper.change_to_relative_path(path)
                self.csv_listbox.insert(END, relative_path)
            else:
                print(f"{path} is not a csv file and will not be imported.")
                continue

        if self.csv_listbox.index(END) == 0:
            print("No valid CSV files found to add.")
        else:
            print("Valid CSV files found.")

    def clear_csv_listbox(self):
        """
        Clears the csv file listbox and disables the related buttons
        :return: None
        """
        self.csv_listbox.delete(0, END)
        self.csv_file_path_list = []
        self.date_folder_combobox.current(0)
        self.abs_path_display_label.config(text="Path Displayed Here")

    def send_csv_to_generate_data(self):
        """
        For each csv file dragged into the widget, send the full path to parse through the data and generate the
        data reports.
        :return: None
        """
        if self.csv_listbox.get(0, END):
            ggd = generate_graph_data.GenerateGraphData()
            graph_path = ""

            for path in self.csv_file_path_list:
                self.csv_file_path = path
                self.graph_paths_per_csv, self.full_line_report = ggd.generate_reports(path)
                # Format path to open to this dir in windows explorer
                graph_path = helper.get_graph_path(path).replace("/", "\\")

            if self.date_folder_combobox.get() != "-- Select Date --":
                subprocess.Popen(f"explorer {graph_path}")
        else:
            print("Please add csv files to the csv listbox via file drag-and-drop, or using the date dropdown menu.")

    def send_email_report(self):
        """
        For each graph directory, send the full path to EmailReport() to generate the email
        body and send the email.
        :return:
        """
        if self.csv_listbox.index(END) != 0 and self.recipient_address_listbox.index(END) != 0:
            self.send_csv_to_generate_data()
            recipient_email_addresses = self.recipient_address_listbox.get(0, END)
            for recipient in recipient_email_addresses:
                for csv_paths_list in self.graph_paths_per_csv:
                    er = email_report.EmailReport(csv_paths_list, self.csv_file_path, recipient,
                                                  self.full_line_report)
                    er.setup_email_properties()
                    email = er.create_email_body()
                    er.finalize_send_email(email)
        else:
            print("Can't send the email report.  User must add csv files in Step 1 and add email addresses to the "
                  "recipient listbox in Step 2.")

    def open_settings_window(self):
        """
        Create new GUI window to house all Settings controls under the Edit menu bar item.
        :return:
        """
        from gui import sender_email_ui
        sender_email_ui.SenderEmail()
