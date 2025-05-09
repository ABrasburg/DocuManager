from sqlalchemy import Column, Integer, DateTime, Float
from db import Base


class IdZeta(Base):
    __tablename__ = "idzeta"
    id = Column(Integer, primary_key=True, index=True)
    contador = Column(Integer, default=0)