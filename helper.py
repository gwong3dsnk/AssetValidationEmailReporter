import os


def graph_directory_exists(csv_dir_path):
    print(csv_dir_path)
    if not os.path.exists(csv_dir_path):
        print(f"The graph directory doesn't exist.  Creating it now at {csv_dir_path}")
        os.makedirs(csv_dir_path)
