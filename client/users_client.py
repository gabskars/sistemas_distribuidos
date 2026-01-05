import requests

resp = requests.post(
    "http://users:5000/users",
    json={"nome": "Ana", "perfil": "Paciente"}
)

print(resp.json())