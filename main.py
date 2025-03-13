
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine # type: ignore
from sqlalchemy.orm import sessionmaker, declarative_base # type: ignore
from sqlalchemy import Column, Integer, String, Text # type: ignore

import os

app = FastAPI()

# Инициализация базы данных
DATABASE_URL = os.getenv("DATABASE_URL")  # Railway автоматически предоставит URL

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Модель таблицы сообщений
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message = Column(Text)

# Создание таблиц
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency для получения сессии
async def get_db():
    async with SessionLocal() as session:
        yield session

class MessageCreate(BaseModel):
    user_id: int
    message: str

@app.post("/add_message")
async def add_message(msg: MessageCreate, db: AsyncSession = Depends(get_db)):
    new_message = Message(user_id=msg.user_id, message=msg.message)
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message

@app.get("/get_message/{message_id}")
async def get_message(message_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM messages WHERE id = :id", {"id": message_id}
    )
    message = result.fetchone()
    if message:
        return {"id": message.id, "user_id": message.user_id, "message": message.message}
    return {"error": "Message not found"}

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



PORT = int(os.getenv("PORT", 8000))  # Берём порт из переменной окружения, если нет — 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)