import requests
from utils.properties import getAqueducteUrl, getAqueducteHashConfigValue


class Authentication():
    def authenticate(hash_config):
        try:
            uri = getAqueducteUrl() + 'external-app-config/' + hash_config
            response = requests.get(uri)

            if response.status_code != 200:
                return False

            externalAppConfig = response.json()['data']
            if getAqueducteHashConfigValue() == externalAppConfig['hashConfig']:
                return True

            return False
        except Exception:
            return False
