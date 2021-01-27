from resources.upload_geo_files import Upload_Geo_Files
from resources.geo_data import Geo_Data, Geo_Data_Fields, Geo_Data_Delete, Generate_Import_Geo_Data_Csv
from resources.geo_data_history import Geo_Data_History, Geo_Data_History_Delete_By_Id, Geo_Data_History_Delete_All
from auth.authentication import Authentication
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/aquegeo'
api = Api(app)


@app.before_request
def auth_filter():
    hash_config = request.headers.get('hash-config')
    if hash_config == None:
        return make_response(
            jsonify({'message': '\'hash-config\' header is not present.'}), 401)

    is_auth = Authentication.authenticate(hash_config)

    if is_auth == False:
        return make_response(jsonify({'message': 'Inform a \'hash-config\'valid to access API'}), 401)


api.add_resource(Upload_Geo_Files, '/aquegeo/upload-geo-files')
api.add_resource(Geo_Data, '/aquegeo/geo-data')
api.add_resource(Geo_Data_Fields, '/aquegeo/geo-data/<dataset_name>/fields')
api.add_resource(Geo_Data_Delete, '/aquegeo/geo-data')

api.add_resource(Generate_Import_Geo_Data_Csv,
                 '/aquegeo/geo-data/generate-import-csv/user-id/<user_id>/task-id/<task_id>')

api.add_resource(Geo_Data_History, '/aquegeo/geo-data-history')
api.add_resource(Geo_Data_History_Delete_By_Id,
                 '/aquegeo/geo-data-history/<id>')
api.add_resource(Geo_Data_History_Delete_All,
                 '/aquegeo/geo-data-history/erase')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333)
