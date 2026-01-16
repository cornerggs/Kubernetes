from kafka import KafkaConsumer
import psycopg2
import json
import os
import time


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "etudiants")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "etudiants")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")


def connect_postgres(max_retries: int = 30, sleep_seconds: float = 2.0):
    last_err = None
    for _ in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
            )
            return conn
        except Exception as e:
            last_err = e
            print(f"[integration] waiting for postgres: {e}")
            time.sleep(sleep_seconds)
    raise last_err


def connect_kafka_consumer(max_retries: int = 30, sleep_seconds: float = 2.0):
    last_err = None
    for _ in range(max_retries):
        try:
            return KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            )
        except Exception as e:
            last_err = e
            print(f"[integration] waiting for kafka: {e}")
            time.sleep(sleep_seconds)
    raise last_err


conn = connect_postgres()
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS etudiants (
        id SERIAL PRIMARY KEY,
        nom VARCHAR(50),
        prenom VARCHAR(50)
    );
    """
)
conn.commit()

consumer = connect_kafka_consumer()

for msg in consumer:
    e = msg.value
    try:
        cur.execute(
            "INSERT INTO etudiants (nom, prenom) VALUES (%s, %s)",
            (e.get("nom"), e.get("prenom")),
        )
        conn.commit()
        print(f"[integration] inserted etudiant nom={e.get('nom')} prenom={e.get('prenom')}")
    except Exception as ex:
        conn.rollback()
        print(f"[integration] error inserting message={e} err={ex}")
