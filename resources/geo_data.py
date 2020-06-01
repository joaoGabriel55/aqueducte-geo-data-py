import json
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from exceptions.data_exception import Data_Exception


from services.geo_data_service import Geo_Data_Service


class Geo_Data(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def get(self):
        try:
            data = self.service.getAllDataSets()
            return make_response(jsonify({'data': data}), 200)
        except Exception as e:
            return make_response(jsonify({'error': e}), 500)


class Geo_Data_Fields(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def get(self, dataset_name):
        try:
            data = self.service.getDataSetFields(dataset_name)
            return make_response(jsonify({'data': data}), 200)
        except Exception as e:
            return make_response(jsonify({'error': e}), 500)


class Generate_Geo_Data_Csv(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def post(self, dataset_name):
        try:
            geojsonField = request.args.get('geojson_field')
            hash = self.service.generateDatasetCsv(
                dataset_name, geojsonField
            )
            return make_response(jsonify({'hash_folder': hash}), 200)
        except Exception:
            raise Data_Exception('Error ', status_code=500)


class Import_HDFS_Geo_Data_Csv(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def post(self, task_id, user_id, hash_folder, dataset_name):
        try:
            self.service.importDatasetCsv(
                task_id, user_id, hash_folder, dataset_name
            )
            return make_response(jsonify({'data': 'imported'}), 200)
        except Exception:
            raise Data_Exception('Import error error', status_code=500)
            # print('ERROR', e)
            # return make_response(jsonify({'error': json.dumps(e)}), 500)


class Geo_Data_Delete_By_Name(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def delete(self, dataset_name):
        try:
            self.service.deleteDataSet(dataset_name)
            return make_response(jsonify({}), 204)
        except Exception as e:
            return make_response(jsonify({'error': e}), 500)
