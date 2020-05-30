from utils.properties import getDbHost, getDbPort, getDbUser, getDbPassword, getDbName

import psycopg2 as db

def dbConnection():
    connection = db.connect(host=getDbHost(), database=getDbName(), port=getDbPort(),
                            user=getDbUser(), password=getDbPassword())
    return connection
