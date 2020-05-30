import os
import subprocess
import pathlib

import random
import shutil

from utils.properties import getDbHost, getDbPort, getDbUser, getDbPassword, getDbName
from utils.folder_files import checkIfFolderExists, TEMP_FOLDER

def allowedFilesType(filename):
    types = ['cpg', 'dbf', 'prj', 'sbn', 'sbx', 'shp', 'shp.xml', 'shx']
    for typeFile in types:
        if typeFile in str(filename).lower():
            return True


def uploadGeoFiles(folder):
    importCmd = "ogr2ogr -f PostgreSQL " + \
        "PG:'host=" + getDbHost() + \
        " port=" + getDbPort() + \
        " user=" + getDbUser() + \
        " dbname=" + getDbName() + \
        " password=" + getDbPassword() + \
        "' " + folder + "/"
    result = os.system(importCmd)
    if result != 0:
        shutil.rmtree(TEMP_FOLDER)
        raise Exception("Import files error!")


class Upload_Files_Service():

    def uploadFiles(self, files):
        hash = random.getrandbits(128)
        checkIfFolderExists(TEMP_FOLDER)

        path = TEMP_FOLDER + "/" + str(hash)
        print(path)
        try:
            if checkIfFolderExists(path) == False:
                for file in files:
                    if file and allowedFilesType(file.filename):
                        file.save(os.path.join(path, file.filename))
                    else:
                        shutil.rmtree(path)
                        raise Exception('Wrong type')

                uploadGeoFiles(path)
        except OSError as e:
            shutil.rmtree(path)
            print("Creation of the directory %s failed" % path)
            raise Exception(e.strerror)

        shutil.rmtree(path)
