from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import sqlite3

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.secret_key = 'your_secret_key'

DBPATH = "./database.db"

def init_db():
    with sqlite3.connect(DBPATH) as connection:
        sql_statements = [
            """CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contents TEXT NOT NULL
            );""",
            """CREATE TRIGGER limit_messages AFTER INSERT ON messages
                BEGIN
                    DELETE FROM messages WHERE id NOT IN (SELECT id FROM messages ORDER BY id DESC LIMIT 3);
                END;"""]
        cursor = connection.cursor()
        for statement in sql_statements:
            cursor.execute(statement)
        connection.commit()

def db_get() -> str:
    if not os.path.exists(DBPATH):
        init_db()
    with sqlite3.connect(DBPATH) as connection:
        query = """SELECT contents FROM messages ORDER BY ID ASC"""
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        return jsonify(res)

def db_post(message: str):
    if not os.path.exists(DBPATH):
        init_db()
    with sqlite3.connect(DBPATH) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO messages (contents) VALUES (?);", (message,))
        connection.commit()

@socketio.on('get')
def handle_get():
    emit('update', db_get())

@socketio.on('post')
def handle_post(msg):
    db_post(msg)
    emit('update', db_get())

"""
@app.route("/post/<path:message>")
def post_message(message):
    db_post(message)
    return db_get()

@app.route("/get")
def get_messages():
    return db_get()
"""
