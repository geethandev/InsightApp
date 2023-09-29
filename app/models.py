from sqlalchemy import Column, Integer, String, ForeignKey, Boolean,DateTime,func,LargeBinary
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String, nullable=False)
    avatar = Column(LargeBinary)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    
