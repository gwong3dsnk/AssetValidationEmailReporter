import os, json
from datetime import date

CSV_SOURCE_DIR = "Desktop/GabeWong-UbisoftTest/TechnicalTest/csv_source_files"
PROJ_DATA_DIR = "Desktop/GabeWong-UbisoftTest/TechnicalTest/proj_data"


def directory_exists(dir_path):
    """
    Check if the Graph img directory exists.  If not, create it recursively.
    :param dir_path: (str)
    :return:
    """
    if not os.path.exists(dir_path):
        print(f"Directory doesn't exist.  Creating it now at {dir_path}")
        os.makedirs(dir_path)


def get_current_date():
    """
    Get todays date in format YYYY-MM-DD
    :return: current_date
    """
    current_date = date.today()
    return current_date


def get_capture_type(path):
    """
    Isolate the capture type string from a given path.  Capture type pertains to the method in which the capture
    was done in UE.  Manual Selection, by specific content browser dir, etc...
    :param path: (str)
    :return capture_type: (str)
    """
    # Take into account if path param includes the filename.fileextension at the end or not.

    if "." in path:
        if "/Graphs/" in path:
            path_split = path.split("/")
            capture_type = path_split[len(path_split) - 2]
        else:
            capture_type = path.rpartition("/")[2].replace(".csv", "")
    else:
        path_split = path.split("/")
        capture_type = path_split[len(path_split) - 1]

    return capture_type


def get_graph_path(path):
    return f"{path.rpartition('/')[0]}/Graphs"


def get_working_dir_path():
    user_home_dir = os.path.expanduser('~')
    insert_path_token = check_for_onedrive()
    working_dir = os.path.join(user_home_dir, insert_path_token, CSV_SOURCE_DIR)
    working_dir.replace("\\", "/")
    proj_data_dir = os.path.join(user_home_dir, insert_path_token, PROJ_DATA_DIR)
    proj_data_dir.replace("\\", "/")

    return working_dir, proj_data_dir


def change_to_relative_path(path):
    file_path_clean = path.replace("\\", "/")
    path_split = file_path_clean.split("/")
    path_segment = os.path.join(path_split[len(path_split) - 2],
                                path_split[len(path_split) - 1]).replace("\\", "/")
    relative_path = f".../{path_segment}"
    return relative_path, file_path_clean


def verify_data_directory():
    # Verify data folder exists
    working_dir, proj_data_dir = get_working_dir_path()
    directory_exists(working_dir)
    directory_exists(proj_data_dir)
    return proj_data_dir


def check_for_onedrive():
    current_wd = os.getcwd()
    if "OneDrive" in current_wd:
        insert_path_token = "OneDrive"
    else:
        insert_path_token = ""

    return insert_path_token


def verify_data_files(proj_data_dir):
    address_book_file_path = os.path.join(proj_data_dir, "address_book.txt")
    presets_file_path = os.path.join(proj_data_dir, "presets.json")
    sender_email_data_path = os.path.join(proj_data_dir, "sender_email_data.json")

    new_email_dict = {
        "email_from_address": "",
        "email_from_password": "",
        "smtp_server_address": "",
        "smtp_server_port": ""
    }

    # If address book file doesn't exist, create it and leave it empty.
    if not os.path.isfile(address_book_file_path):
        with open(address_book_file_path, "w") as new_file:
            new_file.write("")

    # If presets file doesn't exist (or if it does and is empty), create it and populate it with template data.
    if not os.path.isfile(presets_file_path):
        with open(presets_file_path, "w") as new_file:
            new_file.write("")

    if not os.path.isfile(sender_email_data_path):
        with open(sender_email_data_path, "w") as new_file:
            json.dump(new_email_dict, new_file)
        print("ERROR: No sender email information found.  Email report will not be sent.  Please enter sender email"
              "data in the Edit Menu -> Settings and save it.")
