from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

from services.upload_files_service import Upload_Files_Service


class Upload_Geo_Files(Resource):
    service = None

    def __init__(self):
        self.service = Upload_Files_Service()

    def post(self):
        files = request.files.getlist("file")

        try:
            self.service.uploadFiles(files)
            return make_response(jsonify({'data': 'imported geo files'}), 201)
        except OSError as e:
            return make_response(jsonify({'error': e.strerror}), 500)
