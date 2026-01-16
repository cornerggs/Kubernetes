from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "etudiants")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

@app.route("/etudiants", methods=["GET"])
def liste():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT nom, prenom FROM etudiants ORDER BY id DESC")
        rows = cur.fetchall()
        return jsonify([{"nom": r[0], "prenom": r[1]} for r in rows])
    finally:
        conn.close()


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

app.run(host="0.0.0.0", port=5000)
