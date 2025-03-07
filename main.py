
from fastapi import FastAPI

app = FastAPI()

# # 🔹 Функция для получения соединения с БД
# def get_db_connection():
#     conn = sqlite3.connect("mybase.db", check_same_thread=False)
#     return conn

# # 🔹 Создаём таблицу (вызываем 1 раз при старте)
# def create_tables():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS messages (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             time_stamp TEXT,
#             user_id INTEGER,
#             message TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()

# # Вызываем создание таблицы при старте
# create_tables()

# Для проверки, что сервер работает
@app.get("/")
async def root():
    return {"status": "API server is running"}

@app.get("/hello_world")
def hello_world():
    return {"message": "Hello world! version !Docker"}

@app.get("/sum")
def sum_numbers(a: int, b: int):
    return {"a": a, "b": b, "sum": a + b}

# class Message(BaseModel):
#     user_id: int
#     message: str

# @app.post("/add_message")
# def add_message(msg: Message):
#     timestamp = datetime.utcnow().isoformat() + "Z"
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO messages (time_stamp, user_id, message) VALUES (?, ?, ?)",
#                    (timestamp, msg.user_id, msg.message))
#     conn.commit()
#     conn.close()  # 🛠 ВАЖНО: Закрываем соединение!
#     return {"time_stamp": timestamp, "user_id": msg.user_id, "message": msg.message}

# @app.post("/get_message")
# def get_message(id: int):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM messages WHERE id=?", (id,))
#     row = cursor.fetchone()
#     conn.close()
#     if row:
#         return {"id": row[0], "time_stamp": row[1], "user_id": row[2], "message": row[3]}
#     return {"error": "Message not found"}

# @app.post("/get_user_messages")
# def get_user_messages(user_id: int):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM messages WHERE user_id=?", (user_id,))
#     rows = cursor.fetchall()
#     conn.close()
#     messages = [{"id": row[0], "time_stamp": row[1], "user_id": row[2], "message": row[3]} for row in rows]
#     return {"user_id": user_id, "messages": messages}



import os
PORT = int(os.getenv("PORT", 8000))  # Берём порт из переменной окружения, если нет — 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)