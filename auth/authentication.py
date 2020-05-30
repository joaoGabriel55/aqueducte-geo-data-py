import requests


class Authentication():
    def authenticate(sgeol_instance, user_token, app_token):
        try:
            headers = {
                'application-token': app_token,
                'user-token': user_token,
                'sgeol_instance': sgeol_instance
            }
            uri = sgeol_instance + "/idm/users/info"
            response = requests.get(uri, headers=headers)
            user_roles = response.json()['roles']
            for role in user_roles:
                if 'gerente' in role['name']:
                    return True

            return False
        except Exception:
            return False
