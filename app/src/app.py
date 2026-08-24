import os

import psycopg
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

app = Flask(__name__)


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "cloudapp"),
        user=os.getenv("DB_USER", "devuser"),
        password=os.getenv("DB_PASSWORD", "devpass"),
    )


@app.get("/health")
def health():
    return jsonify({"status": "UP"})


@app.get("/version")
def version():
    return jsonify({"version": "1.0.0"})


@app.get("/api/users")
def users():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM users ORDER BY id")
            rows = cursor.fetchall()

    return jsonify([
        {"id": row[0], "name": row[1]}
        for row in rows
    ])


@app.get("/api/orders")
def orders():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, user_id, product FROM orders ORDER BY id"
            )
            rows = cursor.fetchall()

    return jsonify([
        {
            "id": row[0],
            "user_id": row[1],
            "product": row[2],
        }
        for row in rows
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)