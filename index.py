import requests

response = requests.post(
    'http://localhost:1028/geo-data/es_rn_ppm_pam_municipios_2017_250_ibge/user-id/abc/import/181222794512273556241867467551530144579'
)
print(response)
