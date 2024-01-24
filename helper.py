import os
from datetime import date


def directory_exists(csv_dir_path):
    """
    Check if the Graph img directory exists.  If not, create it recursively.
    :param csv_dir_path: (str)
    :return:
    """
    if not os.path.exists(csv_dir_path):
        print(f"Directory doesn't exist.  Creating it now at {csv_dir_path}")
        os.makedirs(csv_dir_path)


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
    working_dir = os.path.join(user_home_dir, "Desktop\GabeWong-UbisoftTest\TechnicalTest\DataFiles")

    return working_dir


def change_to_relative_path(path):
    file_path_clean = path.replace("\\", "/")
    path_split = file_path_clean.split("/")
    path_segment = os.path.join(path_split[len(path_split) - 2],
                                path_split[len(path_split) - 1]).replace("\\", "/")
    relative_path = f".../{path_segment}"
    return relative_path, file_path_clean
