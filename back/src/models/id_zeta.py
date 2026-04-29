from sqlalchemy import Column, Integer, ForeignKey
from db import Base


class IdZeta(Base):
    __tablename__ = "idzeta"
    id = Column(Integer, primary_key=True, index=True)
    contador = Column(Integer, default=0)
    farmacia_id = Column(Integer, ForeignKey("farmacia.id"), nullable=False)