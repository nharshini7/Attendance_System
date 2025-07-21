# backend/app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from register import collect_faces
from recognize import recognize_faces
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # <-- This allows requests from localhost:5173

@app.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400

    success = collect_faces(name)
    return jsonify({"success": success})

@app.route('/recognize', methods=['GET'])
def recognize():
    results = recognize_faces()
    return jsonify(results)

@app.route('/summary', methods=['GET'])
def summary():
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = f"data/Attendance_{today}.csv"
    if not os.path.exists(filepath):
        return jsonify({"count": 0, "names": []})

    with open(filepath, 'r') as f:
        lines = f.readlines()[1:]  # Skip header
        names = [line.split(',')[0] for line in lines]

    return jsonify({"count": len(set(names)), "names": list(set(names))})

@app.route('/download')
def download_csv():
    date = request.args.get("date")
    path = f"data/Attendance_{date}.csv"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
