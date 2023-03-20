import requests

'''URL_SERVIDOR = 'http://140.84.179.17:80'
PAGINA = "/users"

request.post(URL_SERVIDOR+PAGINA, )'''

headers = {'Accept': 'application/json'}

r = requests.get('http://140.84.179.17:80/users', headers=headers)

print(f"Response: {r.json()}")