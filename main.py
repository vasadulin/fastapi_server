from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import sqlite3

app = FastAPI()

# Инициализация базы данных
conn = sqlite3.connect("mybase.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_stamp TEXT,
        user_id INTEGER,
        message TEXT
    )
""")
conn.commit()

@app.get("/hello_world")
def hello_world():
    return {"message": "Hello world! version !Docker"}

@app.get("/sum")
def sum_numbers(a: int, b: int):
    return {"a": a, "b": b, "sum": a + b}

class Message(BaseModel):
    user_id: int
    message: str

@app.post("/add_message")
def add_message(msg: Message):
    timestamp = datetime.utcnow().isoformat() + "Z"
    cursor.execute("INSERT INTO messages (time_stamp, user_id, message) VALUES (?, ?, ?)",
                   (timestamp, msg.user_id, msg.message))
    conn.commit()
    return {"time_stamp": timestamp, "user_id": msg.user_id, "message": msg.message}

@app.post("/get_message")
def get_message(id: int):
    cursor.execute("SELECT * FROM messages WHERE id=?", (id,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "time_stamp": row[1], "user_id": row[2], "message": row[3]}
    return {"error": "Message not found"}

@app.post("/get_user_messages")
def get_user_messages(user_id: int):
    cursor.execute("SELECT * FROM messages WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    messages = [{"id": row[0], "time_stamp": row[1], "user_id": row[2], "message": row[3]} for row in rows]
    return {"user_id": user_id, "messages": messages}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
