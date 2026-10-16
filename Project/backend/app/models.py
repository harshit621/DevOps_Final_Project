from sqlalchemy import Column, Integer, String
from app.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    status = Column(String, default="Available") # Available, Assigned, Maintenance