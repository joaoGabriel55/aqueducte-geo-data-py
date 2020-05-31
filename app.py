from resources.upload_geo_files import Upload_Geo_Files
from resources.geo_data import Geo_Data, Geo_Data_Delete_By_Name, Geo_Data_Fields, Generate_Geo_Data_Csv, Import_HDFS_Geo_Data_Csv
from auth.authentication import Authentication
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


@app.before_request
def auth_filter():
    sgeol_instance = request.headers.get('sgeol-instance')
    user_token = request.headers.get('user-token')
    app_token = request.headers.get('application-token')
    if user_token == None or sgeol_instance == None or app_token == None:
        return make_response(
            jsonify(
                {'message': '\'application-token\', \'user-token\' or \'sgeol-instance\' is not present.'}
            ), 401)

    is_auth = Authentication.authenticate(
        sgeol_instance, user_token, app_token
    )
    if is_auth == False:
        return make_response(jsonify({'message': 'You do not have \'gerente\' role to access API'}), 401)


api.add_resource(Upload_Geo_Files, '/upload-geo-files')
api.add_resource(Geo_Data, '/geo-data')
api.add_resource(Geo_Data_Fields, '/geo-data/<dataset_name>/fields')
api.add_resource(Geo_Data_Delete_By_Name, '/geo-data/<dataset_name>')
api.add_resource(Generate_Geo_Data_Csv, '/geo-data/<dataset_name>/csv')
api.add_resource(
    Import_HDFS_Geo_Data_Csv,
    '/geo-data/<dataset_name>/task-id/<task_id>/user-id/<user_id>/import/<hash_folder>'
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333)
