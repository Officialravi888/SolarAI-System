from sqlalchemy import Column, Integer, String, Float
from db import Base

class SolarData(Base):
    __tablename__ = "solar_data"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String)
    solar_generation = Column(Float)
    month = Column(String)