from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

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


class Geo_Data_By_Name(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def get(self, data_set_name):
        try:
            geojsonField = request.args.get('geojson_field')
            data = self.service.getDataSet(data_set_name, geojsonField)
            return make_response(jsonify({'data': data}), 200)
        except Exception as e:
            return make_response(jsonify({'error': e}), 500)


class Geo_Data_Delete_By_Name(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def delete(self, data_set_name):
        try:
            self.service.deleteDataSet(data_set_name)
            return make_response(jsonify({}), 204)
        except Exception as e:
            return make_response(jsonify({'error': e}), 500)
