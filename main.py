import helper
from gui import ui

if __name__ == "__main__":
    proj_data_dir = helper.verify_data_directory()
    helper.verify_data_files(proj_data_dir)
    ui.ReporterUI()
