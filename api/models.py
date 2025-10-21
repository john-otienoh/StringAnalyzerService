from sqlalchemy import Integer, String, Boolean, DateTime, JSON, Column
from sqlalchemy.sql import func
from .database import Base



class Strings(Base):
    __tablename__ = "strings"
    id = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=False, unique=True)
    properties = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())