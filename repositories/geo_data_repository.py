import json
from datetime import datetime as dt

from exceptions.data_exception import Data_Exception
import psycopg2
import time
from utils.db_connection import dbConnection


class Geo_Data_Repository(object):

    def createDatasetHistoryTable(self):
        try:
            db = dbConnection()
            cursor = db.cursor()

            createTable = "CREATE TABLE IF NOT EXISTS public.dataset_history (id serial PRIMARY KEY, dataset_name varchar(255) NOT NULL, num_elements integer NOT NULL, date_upload TIMESTAMP WITHOUT TIME ZONE NOT NULL);"
            cursor.execute(createTable)
            db.commit()

            db.close()
            cursor.close()
        except Exception as e:
            print(e)
            raise Exception('Error! into create dataset_history table')

    def insertDatasetHistory(self, dataset_name, num_elements):
        try:
            db = dbConnection()
            cursor = db.cursor()
            now = dt.now()
            print(now.year, now.month, now.day,
                  now.hour, now.minute, now.second)
            cursor.execute("INSERT INTO public.dataset_history (dataset_name, num_elements, date_upload) VALUES(%s, %s, %s)",
                           (dataset_name, num_elements, psycopg2.Timestamp(now.year, now.month, now.day, now.hour, now.minute, now.second)))
            db.commit()
            db.close()
            cursor.close()
        except Exception as e:
            print(e)
            raise Exception('Error! into create dataset_history')

    def deleteDatasetHistory(self, id):
        try:
            db = dbConnection()
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM public.dataset_history WHERE id=" + id + ";")
            db.commit()
            db.close()
            cursor.close()
        except Exception as e:
            print(e)
            raise Exception('Error! into delete dataset_history')

    def dropTableDatasetHistory(self):
        try:
            db = dbConnection()
            cursor = db.cursor()
            cursor.execute(
                "DROP TABLE public.dataset_history;")
            db.commit()
            db.close()
            cursor.close()
        except Exception as e:
            print(e)
            raise Exception('Error! into delete dataset_history table')

    def datetimeConverter(self, o):
        if isinstance(o, dt):
            return o.__str__()

    def selectDatasetsHistory(self, limit):
        try:
            db = dbConnection()
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM public.dataset_history ORDER BY date_upload DESC LIMIT " + limit + ";")
            rows = cursor.fetchall()

            if rows == None:
                raise Exception('Error! into retrieve dataset_history')

            response = []
            for row in rows:
                jsonStr = json.dumps(
                    row, ensure_ascii=False, default=self.datetimeConverter)
                result = json.loads(jsonStr)
                jsonData = {
                    "id": result[0],
                    "dataset": result[1],
                    "num_elements": result[2],
                    "upload_date": result[3]
                }
                response.append(jsonData)

            db.commit()
            db.close()
            cursor.close()
            return response
        except Exception as e:
            print(e)
            raise Exception('Error! internal error')

    def showAllDataSets(self):
        try:
            showTablesQuery = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'public'"
            db = dbConnection()
            cursor = db.cursor()

            cursor.execute(showTablesQuery)

            result = cursor.fetchall()

            if result == None:
                raise Data_Exception

            response = []
            for elem in result:
                jsonStr = json.dumps(elem, ensure_ascii=False)
                table = json.loads(jsonStr)[1]
                if table != 'spatial_ref_sys' and table != 'dataset_history':
                    sqlCount = 'SELECT count(*) from ' + table
                    cursor.execute(sqlCount)
                    count = cursor.fetchone()
                    elem = {
                        'dataset': table,
                        'num_elements': count[0]
                    }
                    response.append(elem)

            db.close()
            return response
        except Exception:
            raise Data_Exception(Exception('Error! into fetch all datasets'))

    def getDataSetFields(self, datasetName):
        queryColumns = "SELECT column_name " +\
            "FROM information_schema.columns " +\
            "WHERE table_name = '" + datasetName + "'"
        db = dbConnection()
        cursor = db.cursor()
        cursor.execute(queryColumns)
        columns = cursor.fetchall()

        if columns == None:
            raise Data_Exception

        response = []
        for column in columns:
            jsonStr = json.dumps(column, ensure_ascii=False)
            response.append(json.loads(jsonStr)[0])

        db.close()
        return response

    def getDataSet(self, datasetName, geojsonField):
        try:
            response = self.getDataSetFields(datasetName)
            response.remove(geojsonField)

            columns = ','.join(response)

            query = "SELECT row_to_json(row) FROM " + \
                "(SELECT " + columns + ", ST_AsGeoJSON(" + geojsonField + \
                ") as geojson FROM " + datasetName + ") row"
            db = dbConnection()
            cursor = db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            if result == None:
                db.close()
                raise Data_Exception

            db.close()
            return result
        except Exception:
            raise Data_Exception(
                Exception('Error! into fetch data set ' + datasetName))

    def deleteDataSet(self, datasetName):
        try:
            datasets = self.showAllDataSets()
            datasets = list(map(lambda el: el['dataset'], datasets))
            if datasetName not in datasets:
                return False

            dropTable = "DROP TABLE IF EXISTS " + datasetName
            db = dbConnection()
            cursor = db.cursor()
            cursor.execute(dropTable)
            db.commit()
            db.close()
            return True
        except psycopg2.Error as e:
            raise Exception('Error! into delete dataset')
