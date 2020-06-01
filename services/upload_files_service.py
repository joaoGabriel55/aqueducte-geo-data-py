import os
import subprocess

import random
import shutil

from utils.properties import getDbHost, getDbPort, getDbUser, getDbPassword, getDbName
from utils.folder_files import checkIfFolderExists, TEMP_FOLDER
from repositories.geo_data_repository import Geo_Data_Repository


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
    print(importCmd)
    result = os.system(importCmd)
    if result != 0:
        shutil.rmtree(folder)
        raise Exception("Import files error!")


class Upload_Files_Service(object):

    def uploadFiles(self, files):
        hash = random.getrandbits(128)
        checkIfFolderExists(TEMP_FOLDER)
        path = TEMP_FOLDER + "/" + str(hash)

        try:
            if checkIfFolderExists(path) == False:
                repository = Geo_Data_Repository()
                datasets = repository.showAllDataSets()
                for file in files:
                    if file and allowedFilesType(file.filename):
                        if len(datasets) != 0:
                            for data in datasets:
                                dataset = data['dataset']
                                if dataset in file.filename:
                                    repository.deleteDataSet(dataset)

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
