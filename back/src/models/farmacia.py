from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base


class Farmacia(Base):
    __tablename__ = "farmacia"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False, unique=True)
