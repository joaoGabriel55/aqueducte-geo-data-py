import json
from exceptions.data_exception import Data_Exception
from utils.db_connection import dbConnection


class Geo_Data_Repository(object):

    db = None

    def __init__(self):
        self.db = dbConnection()

    def showAllDataSets(self):
        try:
            showTablesQuery = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'public'"
            self.db.execute(showTablesQuery)
            result = self.db.fetchall()

            if result == None:
                raise Data_Exception

            response = []
            for elem in result:
                jsonStr = json.dumps(elem, ensure_ascii=False)
                response.append(json.loads(jsonStr)[1])

            self.db.close()
            return response
        except Exception:
            raise Data_Exception(Exception('Error! into fetch all datasets'))

    def getDataSet(self, datasetName, geojsonField):
        try:
            print(type(geojsonField))
            queryColumns = "SELECT column_name " +\
                "FROM information_schema.columns " +\
                "WHERE table_name = '" + datasetName + "'"
            self.db.execute(queryColumns)
            columns = self.db.fetchall()

            if columns == None:
                raise Data_Exception

            response = []
            for column in columns:
                jsonStr = json.dumps(column, ensure_ascii=False)
                response.append(json.loads(jsonStr)[0])

            if geojsonField != None:
                response.remove(geojsonField)
            
            columns = ','.join(response)

            query = None
            if geojsonField != None or len(geojsonField)>0:
                query = "SELECT row_to_json(row) FROM " + \
                    "(SELECT " + columns + ", ST_AsGeoJSON(" + geojsonField + \
                    ") as geojson FROM " + datasetName + ") row"
            else:
                query = "SELECT row_to_json(row) FROM " + \
                    "(SELECT " + columns + " FROM " + datasetName + ") row"

            self.db.execute(query)
            result = self.db.fetchall()

            if result == None:
                raise Data_Exception

            response = []
            for elem in result:
                jsonStr = json.dumps(elem, ensure_ascii=True).encode('UTF-8')
                response.append(json.loads(jsonStr)[0])

            if geojsonField != None:
                for elem in response:
                    elem['geojson'] = json.loads(elem['geojson'])

            self.db.close()
            return response
        except Exception:
            raise Data_Exception(
                Exception('Error! into fetch data set ' + datasetName))

    def deleteDataSet(self, parameter_list):
        pass
