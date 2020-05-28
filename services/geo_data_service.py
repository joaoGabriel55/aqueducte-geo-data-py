from exceptions.data_exception import Data_Exception
from repositories.geo_data_repository import Geo_Data_Repository


class Geo_Data_Service(object):

    repository = None

    def __init__(self):
        self.repository = Geo_Data_Repository()

    def getAllDataSets(self):
        try:
            return self.repository.showAllDataSets()
        except Exception:
            raise Data_Exception(Exception("Error get all datasets"))

    def getDataSet(self, datasetName, geojsonField):
        try:
            return self.repository.getDataSet(datasetName, geojsonField)
        except Exception:
            raise Data_Exception(
                Exception("Error get dataset " + datasetName))

    def deleteDataSet(self, datasetName):
        try:
            return self.repository.deleteDataSet(datasetName)
        except Exception:
            raise Data_Exception(
                Exception("Error delete dataset " + datasetName))
