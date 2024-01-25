import tkinter
from tkinter import *
import helper, os, json

BG_COLOR = "#444444"
LIGHT_GRAY_COLOR = "#eeeeee"


class SenderEmail:
    def __init__(self):
        settings_root_ui = tkinter.Tk()
        settings_root_ui.title("Settings")
        settings_root_ui.minsize(width=300, height=200)
        settings_root_ui.config(padx=20, pady=20, bg=BG_COLOR)

        email_title = Label(
            settings_root_ui,
            text="Sender Email Settings",
            font=("Arial", 14, "bold"),
            bg=BG_COLOR,
            fg="#bcbcbc",
        )
        email_title.grid(column=0, row=0, columnspan=2)

        sender_email_address_label = Label(
            settings_root_ui,
            text="Sender Email Address:",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=LEFT
        )
        sender_email_address_label.grid(column=0, row=1)

        self.sender_email_address_entry = Entry(settings_root_ui, width=25)
        self.sender_email_address_entry.grid(column=1, row=1)

        sender_email_password_label = Label(
            settings_root_ui,
            text="Sender Email Password:",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=LEFT
        )
        sender_email_password_label.grid(column=0, row=2)

        self.sender_email_password_entry = Entry(settings_root_ui, width=25)
        self.sender_email_password_entry.grid(column=1, row=2)

        smtp_server_address_label = Label(
            settings_root_ui,
            text="SMTP Server Address:",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=LEFT
        )
        smtp_server_address_label.grid(column=0, row=3)

        self.smtp_server_address_entry = Entry(settings_root_ui, width=25)
        self.smtp_server_address_entry.grid(column=1, row=3)

        smtp_server_port_label = Label(
            settings_root_ui,
            text="SMTP Server Port:",
            bg=BG_COLOR,
            fg=LIGHT_GRAY_COLOR,
            justify=LEFT
        )
        smtp_server_port_label.grid(column=0, row=4)

        self.smtp_server_port_entry = Entry(settings_root_ui, width=25)
        self.smtp_server_port_entry.grid(column=1, row=4)

        email_info_button = Button(settings_root_ui, text="Save Information", command=self.save_email_information)
        email_info_button.grid(column=0, row=5, columnspan=2, pady=10)

        # Get current email settings
        self.load_email_settings()

        settings_root_ui.mainloop()

    def save_email_information(self):
        """
        Save entered email information to json file - sender_email_data.json.
        :return:
        """
        working_dir = helper.get_working_dir_path()
        json_file = os.path.join(working_dir, "../proj_data/sender_email_data.json")
        with open(json_file, "r") as f:
            contents = json.load(f)
            contents["email_from_address"] = self.sender_email_address_entry.get()
            contents["email_from_password"] = self.sender_email_password_entry.get()
            contents["smtp_server_address"] = self.smtp_server_address_entry.get()
            contents["smtp_server_port"] = self.smtp_server_port_entry.get()
        with open(json_file, "w") as f:
            json.dump(contents, f, indent=4)

    def load_email_settings(self):
        """
        On Settings window show, read the contents from the json file and populate the entry fields.
        :return:
        """
        working_dir = helper.get_working_dir_path()
        json_file = os.path.join(working_dir, "../proj_data/sender_email_data.json")
        with open(json_file, "r") as f:
            contents = json.load(f)
            if contents:
                self.sender_email_address_entry.insert(0, contents["email_from_address"])
                self.sender_email_password_entry.insert(0, contents["email_from_password"])
                self.smtp_server_address_entry.insert(0, contents["smtp_server_address"])
                self.smtp_server_port_entry.insert(0, contents["smtp_server_port"])
