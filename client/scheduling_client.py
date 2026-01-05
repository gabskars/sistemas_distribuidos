import requests

resp = requests.post(
    "http://scheduling:5000/appointments",
    json={
        "paciente": "Ana",
        "medico": "Dr João",
        "horario": "10:00"
    }
)

print(resp.json())