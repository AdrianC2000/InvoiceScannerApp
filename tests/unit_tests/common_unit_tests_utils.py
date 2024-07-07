import os

__PROJECT_NAME = "InvoiceScannerApp"


def cd_to_project_root_path():
    working_directory = os.getcwd()
    project_index = working_directory.find(__PROJECT_NAME)
    project_root_path = working_directory[:project_index + len(__PROJECT_NAME)]
    os.chdir(project_root_path)
