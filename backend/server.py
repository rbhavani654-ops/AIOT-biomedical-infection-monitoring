from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "sample_data.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# create CSV header if not exists
if not os.path.exists(DATA_FILE):
  with open(DATA_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "patient_id", "temperature", "heart_rate", "spo2"])

@app.route("/api/v1/data", methods=["POST"])
def receive_data():
  data = request.get_json(force=True)

  patient_id = data.get("patient_id", "P001")
  temperature = float(data.get("temperature", 0.0))
  heart_rate  = float(data.get("heart_rate", 0.0))
  spo2        = float(data.get("spo2", 0.0))
  timestamp   = datetime.utcnow().isoformat()

  with open(DATA_FILE, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([timestamp, patient_id, temperature, heart_rate, spo2])

  print(f"[{timestamp}] {patient_id} T={temperature} HR={heart_rate} SpO2={spo2}")
  return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
