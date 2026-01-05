from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
appointments = []

@app.route("/appointments", methods=["POST"])
def schedule():
    data = request.json

    # chama validação
    resp = requests.post("http://validation:5000/validate", json=data)
    status = resp.json()["status"]

    appointment = {
        "paciente": data["paciente"],
        "medico": data["medico"],
        "horario": data["horario"],
        "status": status
    }

    appointments.append(appointment)
    return jsonify(appointment)

@app.route("/appointments", methods=["GET"])
def list_appointments():
    return jsonify(appointments)

app.run(host="0.0.0.0", port=5000)