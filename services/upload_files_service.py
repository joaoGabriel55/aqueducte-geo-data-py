import os
import subprocess

import random
import shutil

from utils.properties import getDbHost, getDbPort, getDbUser, getDbPassword, getDbName
from utils.folder_files import checkIfFolderExists, TEMP_FOLDER
from repositories.geo_data_repository import Geo_Data_Repository


def allowedFilesType(files):
    types = ['.dbf', '.prj', '.shp', '.shx']

    # Allow only unique files
    validTypes = set()
    for typeFile in types:
        for file in files:
            if typeFile in str(file.filename).lower():
                validTypes.add(typeFile)

    if len(types) == len(validTypes):
        return True

    return False


def uploadGeoFiles(folder):
    importCmd = "ogr2ogr -f PostgreSQL " + \
        "PG:'host=" + getDbHost() + \
        " port=" + getDbPort() + \
        " user=" + getDbUser() + \
        " dbname=" + getDbName() + \
        " password=" + getDbPassword() + \
        "' -nlt PROMOTE_TO_MULTI " + folder + "/ -skipfailures"
    print(importCmd)
    result = os.system(importCmd)
    if result != 0:
        shutil.rmtree(folder)


class Upload_Files_Service(object):

    def uploadFiles(self, files):
        try:
            if allowedFilesType(files) == False:
                raise Exception('Wrong type')

            hash = random.getrandbits(128)
            checkIfFolderExists(TEMP_FOLDER)
            path = TEMP_FOLDER + "/" + str(hash)

            if checkIfFolderExists(path) == False:
                repository = Geo_Data_Repository()
                datasets = repository.showAllDataSets()
                for file in files:
                    file.filename = file.filename.replace(" ", "_")
                    print(file.filename)
                    if file:
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
                actualDatasets = repository.showAllDataSets()
                for data in actualDatasets:
                    if data['num_elements'] == 0:
                        repository.deleteDataSet(data['dataset'])
                return actualDatasets
        except OSError as e:
            shutil.rmtree(path)
            print("Creation of the directory %s failed" % path)
            raise Exception(e.strerror)

        shutil.rmtree(path)
