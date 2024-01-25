import os, json
from datetime import date


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
    print(f"get_graph_path: {path}")
    return f"{path.rpartition('/')[0]}/Graphs"


def get_working_dir_path():
    user_home_dir = os.path.expanduser('~')
    working_dir = os.path.join(user_home_dir, "Desktop\GabeWong-UbisoftTest\TechnicalTest\csv_source_files")
    working_dir.replace("\\", "/")
    proj_data_dir = os.path.join(user_home_dir, "Desktop\GabeWong-UbisoftTest\TechnicalTest\proj_data")
    proj_data_dir.replace("\\", "/")

    return working_dir, proj_data_dir


def change_to_relative_path(path):
    file_path_clean = path.replace("\\", "/")
    path_split = file_path_clean.split("/")
    path_segment = os.path.join(path_split[len(path_split) - 2],
                                path_split[len(path_split) - 1]).replace("\\", "/")
    relative_path = f".../{path_segment}"
    return relative_path, file_path_clean


def verify_data_directory_and_files():
    # Verify data folder exists
    working_dir, proj_data_dir = get_working_dir_path()
    directory_exists(proj_data_dir)

    # Verify data files exist
    files_to_check = ["address_book.txt", "presets.json", "sender_email_data.json"]

    proj_data_contents = os.listdir(proj_data_dir)
    address_book_file_path = os.path.join(proj_data_dir, files_to_check[0])
    presets_file_path = os.path.join(proj_data_dir, files_to_check[1])
    sender_email_data_path = os.path.join(proj_data_dir, files_to_check[2])

    if files_to_check[0] not in proj_data_contents:
        with open(address_book_file_path, "w") as new_file:
            new_file.write("")

    if files_to_check[1] not in proj_data_contents:
        with open(presets_file_path, "w") as new_file:
            with open("saved/template_data.json", "r") as template_data:
                contents = json.load(template_data)
                json.dump(contents, new_file, indent=4)
    else:
        template_exists = True
        existing_preset_data = []

        # File exists.  Check for init_data key if it exists in the contents first index
        with open(presets_file_path, "r") as file:
            contents = json.load(file)
            if "init_data" not in contents[0]:
                template_exists = False
                existing_preset_data = contents

        # Template data not found at index 0.  Clear the file, add the template data to index 0 and write back to
        # the json file with existing content.
        if not template_exists:
            open(presets_file_path, "w").close()
            with open(presets_file_path, "w") as file:
                with open("saved/template_data.json", "r") as template_data:
                    td_contents = json.load(template_data)
                    existing_preset_data.insert(0, td_contents[0])
                    json.dump(contents, file, indent=4)

    if files_to_check[2] not in proj_data_contents:
        with open(sender_email_data_path, "w") as new_file:
            new_file.write("")
