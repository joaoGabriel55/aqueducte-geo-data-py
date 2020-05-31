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
            cursor = self.db.cursor()

            try:
                cursor.execute(showTablesQuery)
            except Exception as e:
                print(e.message)
                conn = dbConnection()
                cursor = conn.cursor()

            result = cursor.fetchall()

            if result == None:
                raise Data_Exception

            response = []
            for elem in result:
                jsonStr = json.dumps(elem, ensure_ascii=False)
                table = json.loads(jsonStr)[1]
                if table != 'spatial_ref_sys':
                    sqlCount = 'SELECT count(*) from ' + table
                    cursor.execute(sqlCount)
                    count = cursor.fetchone()
                    elem = {
                        'dataset': table,
                        'num_elements': count[0]
                    }
                    response.append(elem)

            self.db.close()
            return response
        except Exception:
            raise Data_Exception(Exception('Error! into fetch all datasets'))

    def getDataSetFields(self, datasetName):
        queryColumns = "SELECT column_name " +\
            "FROM information_schema.columns " +\
            "WHERE table_name = '" + datasetName + "'"

        cursor = self.db.cursor()
        cursor.execute(queryColumns)
        columns = cursor.fetchall()

        if columns == None:
            raise Data_Exception

        response = []
        for column in columns:
            jsonStr = json.dumps(column, ensure_ascii=False)
            response.append(json.loads(jsonStr)[0])

        return response

    def getDataSet(self, datasetName, geojsonField):
        try:
            response = self.getDataSetFields(datasetName)
            response.remove(geojsonField)

            columns = ','.join(response)

            query = "SELECT row_to_json(row) FROM " + \
                "(SELECT " + columns + ", ST_AsGeoJSON(" + geojsonField + \
                ") as geojson FROM " + datasetName + ") row"
            cursor = self.db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            if result == None:
                self.db.close()
                raise Data_Exception

            self.db.close()
            return result
        except Exception:
            raise Data_Exception(
                Exception('Error! into fetch data set ' + datasetName))

    def deleteDataSet(self, datasetName):
        try:
            dropTable = "DROP TABLE " + datasetName
            cursor = self.db.cursor()
            cursor.execute(dropTable)
            self.db.commit()
            self.db.close()
        except Exception:
            raise Data_Exception(Exception('Error! into delete dataset'))
