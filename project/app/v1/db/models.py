from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import declarative_mixin

from datetime import datetime
from .config import Base


@declarative_mixin
class Timestamp:
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), onupdate=datetime.now, default=datetime.utcnow
    )


class FileData(Timestamp, Base):
    __tablename__ = "filedata"

    file_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    filename = Column(String)
    filepath = Column(String)
    filebase64 = Column(LargeBinary)
