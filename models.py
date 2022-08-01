import datetime
from typing import Optional

from database import Base
from sqlalchemy import Text, Integer, Boolean, Column, DateTime


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime,default=datetime.datetime.utcnow())
    deleted_at = Column(DateTime, default=None)

