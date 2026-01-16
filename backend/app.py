from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import os
import time

app = Flask(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "etudiants")

_producer = None


def get_producer(max_retries: int = 5, sleep_seconds: float = 1.0) -> KafkaProducer:
    global _producer
    if _producer is not None:
        return _producer

    last_err = None
    for _ in range(max_retries):
        try:
            _producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            )
            return _producer
        except Exception as e:
            last_err = e
            time.sleep(sleep_seconds)
    raise last_err

@app.route("/etudiants", methods=["POST"])
def ajouter_etudiant():
    data = request.json
    try:
        producer = get_producer()
        producer.send(KAFKA_TOPIC, data)
        producer.flush()
        return jsonify({"status": "Message envoyé à Kafka"}), 201
    except Exception as e:
        return jsonify({"status": "Kafka indisponible", "error": str(e)}), 503

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

