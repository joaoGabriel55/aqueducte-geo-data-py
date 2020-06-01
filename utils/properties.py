import os
from dotenv import load_dotenv

# OR, the same with increased verbosity
load_dotenv(verbose=True)

def getDbHost():
    return str(os.getenv("DB_HOST"))


def getDbPort():
    return str(os.getenv("DB_PORT"))


def getDbUser():
    return str(os.getenv("DB_USER"))


def getDbPassword():
    return str(os.getenv("DB_PASSWORD"))


def getDbName():
    return str(os.getenv("DB_NAME"))


def getAqueconnectUrl():
    return str(os.getenv("AQUECONNECT_URL"))
