from resources.upload_geo_files import Upload_Geo_Files
from resources.geo_data import Geo_Data, Geo_Data_By_Name

from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


@app.before_request
def before_request_func():
    print("before_request is running!")
    # TODO: AUTH


api.add_resource(Upload_Geo_Files, '/upload-geo-files')
api.add_resource(Geo_Data, '/geo-data')
api.add_resource(Geo_Data_By_Name, '/geo-data/<data_set_name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1028)
