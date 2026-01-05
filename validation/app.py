from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/validate", methods=["POST"])
def validate():
    status = random.choice(["APROVADO", "REJEITADO"])
    return jsonify({"status": status})

app.run(host="0.0.0.0", port=5000)