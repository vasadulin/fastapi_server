
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Message
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Создаем таблицы в базе данных при запуске приложения
Base.metadata.create_all(bind=engine)

# Pydantic модели для валидации запросов и ответов
class MessageCreate(BaseModel):
    user_id: int
    message: str

class MessageResponse(BaseModel):
    id: int
    time_stamp: str
    user_id: int
    message: str

class UserMessagesResponse(BaseModel):
    user_id: int
    messages: List[MessageResponse]

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

@app.post("/sum")
async def post_sum(a: int = 1, b: int = 3):
    return {"a": a, "b": b, "sum": a + b}

# Новые эндпоинты для работы с базой данных
@app.post("/add_message", response_model=MessageResponse)
async def add_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = Message(user_id=message.user_id, message=message.message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.post("/get_message", response_model=MessageResponse)
async def get_message(id: int, db: Session = Depends(get_db)):
    db_message = db.query(Message).filter(Message.id == id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@app.post("/get_user_messages", response_model=UserMessagesResponse)
async def get_user_messages(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.user_id == user_id).all()
    return {"user_id": user_id, "messages": messages}

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