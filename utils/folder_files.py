import os
import pathlib

TEMP_FOLDER = 'upload_temp_data'

def checkIfFolderExists(folder):
    if pathlib.Path(folder).exists() == False:
        os.mkdir(folder)
        return False
    return True
