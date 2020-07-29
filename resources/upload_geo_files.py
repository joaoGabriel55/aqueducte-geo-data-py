from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

from services.upload_files_service import Upload_Files_Service


class Upload_Geo_Files(Resource):
    service = None

    def __init__(self):
        self.service = Upload_Files_Service()

    def post(self):
        response = {"errors": [], "success": []}
        files = request.files.getlist("file")
        try:
            result = self.service.uploadFiles(files)

            uniqueFiles = []
            for file in files:
                filename = str(file.filename).split('.')[0]
                filenameFormated = filename.lower().replace(' ', '_')
                if filenameFormated not in uniqueFiles:
                    uniqueFiles.append(filenameFormated)

            for file in uniqueFiles:
                isUploaded = False
                for elem in result:
                    if elem['dataset'] == file:
                        if elem['num_elements'] == 0:
                            response['errors'].append(elem['dataset'])
                        else:
                            response['success'].append(elem['dataset'])
                        isUploaded = True
                        break
                if isUploaded == False:
                    response['errors'].append(file)

            uniqueSuccess = list(set(response['success']))
            uniqueErrors = list(set(response['errors']))
            response['success'] = uniqueSuccess
            response['errors'] = uniqueErrors

            return make_response(jsonify({'data': response}), 201)
        except OSError as e:
            print(e)
            return make_response(jsonify({'error': 'imported geo files'}), 500)
