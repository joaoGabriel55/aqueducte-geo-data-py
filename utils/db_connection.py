from utils.properties import getDbHost, getDbPort, getDbUser, getDbPassword, getDbName

import psycopg2 as database


def dbConnection():
    connection = database.connect(host=getDbHost(), dbname=getDbName(), port=getDbPort(),
                                  user=getDbUser(), password=getDbPassword())
    return connection
