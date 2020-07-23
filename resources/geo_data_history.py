import json
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from exceptions.data_exception import Data_Exception


from services.geo_data_service import Geo_Data_Service


class Geo_Data_History(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def get(self):
        try:
            result = self.service.getDatasetsHistory()
            return make_response(jsonify(result), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify({'error': 'Internal error in retrieve all history'}), 500)


class Geo_Data_History_Delete_By_Id(Resource):
    service = None

    def __init__(self):
        self.service = Geo_Data_Service()

    def delete(self, id):
        try:
            self.service.deleteDatasetHistory(id)
            return make_response(jsonify({}), 204)
        except Exception as e:
            print(e)
            return make_response(jsonify({'error': 'Internal error in delete history ' + id}), 500)
