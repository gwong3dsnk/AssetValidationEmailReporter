from tkinter import *
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys

BG_COLOR = "#444444"
LIGHT_GRAY_COLOR = "#eeeeee"


class ReporterUI:
    """
    This class generates and displays the GUI
    ...
    Attributes
    ----------
    Pending

    Methods
    ----------
    Pending
    """
    def __init__(self):
        # Use TkinterDnD.Tk() to allow for drag and drop functionality onto widgets
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
        edit_menu.add_command(label="Settings", command=self.do_nothing)
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
        title_label.grid(column=0, row=0, columnspan=3)

        summary_label = Label(
            text="This tool allows you to read in asset validation data_old in CSV format, generate visual graphs, "
                 "and send an email report to specified recipients.",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            wraplength=500,
            justify=LEFT
        )
        summary_label.grid(column=0, row=1, columnspan=3)

        ttk.Separator(self.root_ui, orient=HORIZONTAL).grid(
            column=0,
            row=2,
            columnspan=3,
            sticky="we",
            pady=10
        )

        csv_listbox_label = Label(
            text="STEP 1: Drag and drop 1 or more CSV files into the listbox below.",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
        )
        csv_listbox_label.grid(column=0, row=3, columnspan=3)

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
        file_listbox_frame.grid(column=0, row=4, columnspan=3, pady=10)
        self.csv_listbox.pack()
        self.csv_listbox.drop_target_register(DND_FILES)
        self.csv_listbox.dnd_bind("<<Drop>>", self.drop_inside_csv_listbox)

        self.preview_graph_button = Button(text="Preview Graph(s)")
        self.preview_graph_button.grid(column=0, row=5, sticky="e")

        self.clear_csv_listbox_button = Button(text="Clear CSV Listbox", command=self.clear_csv_listbox)
        self.clear_csv_listbox_button.grid(column=2, row=5, sticky="w")

        email_addresses_listbox_label = Label(
            text="STEP 2: Add email addresses to the ADDRESS BOOK listbox.  Then add the intended recipients "
                 "addresses to the RECIPIENT listbox.",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            wraplength=500,
            justify=LEFT
        )
        email_addresses_listbox_label.grid(column=0, row=6, columnspan=3, pady=10)

        address_book_label = Label(
            text="Address Book",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=CENTER,
            font=("Arial", 10, "bold"),
        )
        address_book_label.grid(column=0, row=7)

        address_book_label = Label(
            text="Recipient(s)",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=CENTER,
            font=("Arial", 10, "bold"),
        )
        address_book_label.grid(column=2, row=7)

        self.address_book_listbox = Listbox(height=4, width=25, selectmode=MULTIPLE)
        self.address_book_listbox.grid(column=0, row=8, columnspan=1, rowspan=2, sticky="nsew", pady=10)

        self.recipient_address_listbox = Listbox(height=4, width=25, selectmode=MULTIPLE)
        self.recipient_address_listbox.grid(column=2, row=8, columnspan=1, rowspan=2, sticky="nsew", pady=10)

        self.add_recipient_button = Button(text=">", width=4)
        self.add_recipient_button.grid(column=1, row=8)

        self.remove_recipient_button = Button(text="<", width=4)
        self.remove_recipient_button.grid(column=1, row=9)

        self.add_new_email_address_entry = Entry()
        self.add_new_email_address_entry.grid(column=0, row=10, sticky="nsew")

        self.clear_recipient_listbox_button = Button(text="Clear Recipients")
        self.clear_recipient_listbox_button.grid(column=2, row=10)

        send_email_report_label = Label(
            text="STEP 3: Send your email report to all recipients by clicking the button below.",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=LEFT
        )
        send_email_report_label.grid(column=0, row=11, columnspan=3)

        self.send_email_report_button = Button(text="Send Email Report", bg="green")
        self.send_email_report_button.grid(column=0, row=12, columnspan=3, pady=10)

        self.end_separator = ttk.Separator(self.root_ui, orient=HORIZONTAL)
        self.end_separator.grid_forget()

        self.log_window = ScrolledText(height=10, width=10)
        self.log_window.grid_forget()

        self.root_ui.mainloop()

    def do_nothing(self):
        pass

    def exit_app(self):
        sys.exit()

    def toggle_log_window_visibility(self):
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
        :param filename (str): String representation of paths for all files dragged and dropped into listbox
        :return clean_path_list (list): List of all paths from files that were dragged and dropped into listbox
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
        # The event variable is a string representation of the drag-and-dropped file paths.  File path str in data_old.
        path_list = self.parse_dropped_files(event.data)

        for path in path_list:
            if path.endswith(".csv"):
                self.csv_listbox.insert(END, path)
            else:
                print(f"{path} is not a csv file and will not be imported.")
                continue

    def clear_csv_listbox(self):
        self.csv_listbox.delete(0, END)
