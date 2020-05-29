import os


def getDbHost():
    return str(os.environ.get("DB_HOST"))


def getDbPort():
    return str(os.environ.get("DB_PORT"))


def getDbUser():
    return str(os.environ.get("DB_USER"))


def getDbPassword():
    return str(os.environ.get("DB_PASSWORD"))


def getDbName():
    return str(os.environ.get("DB_NAME"))


def getAqueconnectUrl():
    return str(os.environ.get("AQUECONNECT_URL"))
