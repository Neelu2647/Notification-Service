from sqlalchemy import Column, Integer, Text, DateTime, func
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, nullable = False)
    message = Column(Text, nullable =  False)
    created_at = Column(DateTime(timezone = True), server_default = func.now(), nullable = False)
    