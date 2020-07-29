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
            print(e)
            return make_response(jsonify({'error': 'Internal error in retrieve datasets'}), 500)


class Geo_Data_Fields(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def get(self, dataset_name):
        try:
            data = self.service.getDataSetFields(dataset_name)
            if len(data) == 0:
                return make_response(jsonify({'error': 'Any field'}), 400)
            return make_response(jsonify({'data': data}), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify({'error': 'Internal error in retrieve dataset [' + dataset_name + '] fields'}), 500)


class Geo_Data_Delete(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def delete(self):
        try:
            response = {"errors": [], "success": []}
            dataset_names = request.json
            for dataset_name in dataset_names:
                result = self.service.deleteDataSet(dataset_name)
                if result:
                    response['success'].append(dataset_name)
                else:
                    response['errors'].append(dataset_name)

            
                return make_response(jsonify(response), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify({'error': 'Internal error in retrieve dataset [' + dataset_name + '] fields'}), 500)


class Generate_Import_Geo_Data_Csv(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def post(self, user_id, task_id):
        response = {"errors": [], "success": []}
        datasets = request.json
        for elem in datasets:
            try:
                hash = self.service.generateDatasetCsv(
                    elem['dataset'], elem['geojson_field']
                )
                try:
                    self.service.importDatasetCsv(
                        task_id, user_id, hash, elem['dataset']
                    )

                    self.service.createDatasetHistory(elem['dataset'])
                    self.service.deleteDataSet(elem['dataset'])
                    response['success'].append(
                        {"dataset": elem['dataset']})
                except Exception as e:
                    print(e)
                    response['errors'].append(
                        {"dataset": elem['dataset'], "error": 'Error at importDatasetCsv method'})
            except Exception as e:
                print(e)
                response['errors'].append(
                    {"dataset": elem['dataset'], "error": 'Error at generateDatasetCsv method'})

        return make_response(jsonify(response), 200)
