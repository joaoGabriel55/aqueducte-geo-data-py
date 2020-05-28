from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

from services.upload_files_service import Upload_Files_Service

class Upload_Geo_Files(Resource):
    # Upload File
    def post(self):
        service = Upload_Files_Service
        files = request.files.getlist("file")

        try:
            service.uploadFiles(self, files)
            data = request.get_json()  # status code
            return make_response(jsonify({'data': data}), 201)
        except OSError as e:
            return make_response(jsonify({'data': e.strerror}), 500)
