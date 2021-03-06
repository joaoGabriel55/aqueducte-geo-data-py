import csv
import random
import json
import requests
import shutil
from requests_toolbelt.multipart.encoder import MultipartEncoder

from utils.folder_files import checkIfFolderExists, TEMP_FOLDER
from utils.properties import getAqueconnectUrl, getAqueducteHashConfigValue
from exceptions.data_exception import Data_Exception
from repositories.geo_data_repository import Geo_Data_Repository

from flask import request


class Geo_Data_Service(object):

    repository = None

    def __init__(self):
        self.repository = Geo_Data_Repository()

    def getDatasetsHistory(self, limit):
        try:
            return self.repository.selectDatasetsHistory(limit)
        except Exception as e:
            print(e)
            raise Data_Exception(Exception("Error get datasets history"))

    def createDatasetHistory(self, dataset):
        try:
            self.repository.createDatasetHistoryTable()
            datasets = self.repository.showAllDataSets()
            for elem in datasets:
                if(dataset == elem['dataset']):
                    print(elem['dataset'], elem['num_elements'])
                    self.repository.insertDatasetHistory(
                        elem['dataset'], elem['num_elements'])
        except Exception as e:
            print(e)
            raise Data_Exception(
                Exception("Error create dataset history - " + dataset))

    def deleteDatasetHistory(self, id):
        try:
            self.repository.deleteDatasetHistory(id)
        except Exception as e:
            print(e)
            raise Data_Exception(
                Exception("Error delete dataset history - " + id))

    def deleteAllDatasetHistory(self):
        try:
            self.repository.dropTableDatasetHistory()
        except Exception as e:
            print(e)
            raise Data_Exception(Exception("Error delete all dataset history"))

    def getAllDataSets(self):
        try:
            return self.repository.showAllDataSets()
        except Exception as e:
            print(e)
            raise Data_Exception(Exception("Error get all datasets"))

    def getDataSetFields(self, datasetName):
        try:
            if datasetName == None or datasetName == '':
                raise Data_Exception(
                    Exception("Error delete dataset " + datasetName))
            return self.repository.getDataSetFields(datasetName)
        except Exception as e:
            print(e)
            raise Data_Exception(
                Exception("Error get dataset " + datasetName))

    def generateDatasetCsv(self, datasetName, geojsonField):
        if datasetName == 'dataset_history':
            raise Exception("Wrong dataset name!")
        if datasetName == None or datasetName == '':
            raise Exception("Dataset name must be informed")
        if geojsonField == None or geojsonField == '':
            raise Exception("Geojson field must be informed")

        result = self.repository.getDataSet(datasetName, geojsonField)

        checkIfFolderExists(TEMP_FOLDER)

        hash = str(random.getrandbits(128))

        path = TEMP_FOLDER + '/' + hash
        checkIfFolderExists(path)

        data_file = open(path + '/' + datasetName + '.csv', 'w')
        csv_writer = csv.writer(data_file)

        count = 0
        for data in result:
            jsonStr = json.dumps(data, ensure_ascii=False)
            jsonObj = json.loads(jsonStr)[0]
            if count == 0:
                # Writing headers of CSV file
                header = jsonObj.keys()
                csv_writer.writerow(header)
                count += 1

            csv_writer.writerow(jsonObj.values())

        data_file.close()
        return hash

    def importDatasetCsv(self, task_id, user_id, hash_folder, dataset_name):
        checkIfFolderExists(TEMP_FOLDER)

        path = TEMP_FOLDER + '/' + str(hash_folder)
        with open(path + "/" + dataset_name + ".csv", "rb") as a_file:
            print(a_file)
            uri = getAqueconnectUrl() + 'file/' + user_id + '/' + \
                task_id + "?path=/geo-data-files/" + dataset_name + '.csv'

            mp_encoder = MultipartEncoder(
                fields={
                    'file': (dataset_name + '.csv', a_file, 'text/csv'),
                }
            )
            hash_config_value = getAqueducteHashConfigValue()

            headers = {
                'hash-config': hash_config_value,
                'Content-Type': mp_encoder.content_type
            }

            response = requests.post(uri, data=mp_encoder, headers=headers)
            shutil.rmtree(path)
            if response.status_code != 201:
                raise Exception("File import failed!")

    def deleteDataSet(self, datasetName):
        try:
            if datasetName == None or datasetName == '':
                raise Exception("Dataset name must be informed")
            return self.repository.deleteDataSet(datasetName)
        except Exception as e:
            print(e)
            raise Exception("Error delete dataset " + datasetName)
