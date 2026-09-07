from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Chathistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer , primary_key=True , index=True)
    user_query = Column(str)
    ai_response = Column(Text)

    