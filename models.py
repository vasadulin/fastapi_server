# models.py
from sqlalchemy import Column, Integer, String, Text
from database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_stamp = Column(String, default=lambda: datetime.utcnow().isoformat() + "Z")
    user_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    