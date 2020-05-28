import os
import psycopg2 as db
import json

HOST = 'localhost'
PORT = 5434
USER = 'postgres'
PASSWORD = 'sgeolpass'
DB_NAME = 'geologia'
FOLDER = 'data/'

connection = db.connect(host=HOST, database=DB_NAME, port=PORT,
                        user=USER, password=PASSWORD)
cur = connection.cursor()

# showTablesQuery = "SELECT row_to_json(row) FROM (SELECT *, ST_AsGeoJSON(wkb_geometry) as geojson FROM es_rn_aglomerado_rural_isolado_p_250_2019_ibge) row"
# showTablesQuery = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'public'"
showTablesQuery = "SELECT column_name FROM information_schema.columns WHERE table_name = 'es_rn_aglomerado_rural_isolado_p_250_2019_ibge' ORDER  BY ordinal_position"
cur.execute(showTablesQuery)

result = cur.fetchall()

response = []

for data in result:
    jsonStr = json.dumps(data, ensure_ascii=False)
    response.append(json.loads(jsonStr)[0])

connection.close()

print(response)

# importQuery = "ogr2ogr -f PostgreSQL " + \
#     "PG:'host=" + HOST + \
#     " port=" + str(PORT) + \
#     " user=" + USER + \
#     " dbname=" + DB_NAME + \
#     " password=" + PASSWORD + \
#     "' " + FOLDER

# os.system(importQuery)
