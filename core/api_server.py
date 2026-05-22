from flask import Flask, request, jsonify

from flask_cors import CORS

from core.jarvis_engine import handle_commands

app = Flask(__name__)

CORS(app)

# ==========================================
# API ROUTE
# ==========================================

@app.route("/jarvis", methods=["POST"])

def jarvis():

    data = request.json

    command = data.get("command")

    response = handle_commands(command)

    return jsonify({

        "response": response

    })

# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000
    )