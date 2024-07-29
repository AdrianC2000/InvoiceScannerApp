import os

from PIL import Image
import numpy as np
from numpy import ndarray

__PROJECT_NAME = "InvoiceScannerApp"


def cd_to_project_root_path():
    working_directory = os.getcwd()
    project_index = working_directory.find(__PROJECT_NAME)
    project_root_path = working_directory[:project_index + len(__PROJECT_NAME)]
    os.chdir(project_root_path)


def load_file(path: str) -> ndarray:
    return np.array(Image.open(path))
