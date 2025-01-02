from sqlalchemy import Column, Integer, String, Float
from .base import Base


class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String)
    property_title = Column(String)
    hotel_id = Column(String, unique=True)
    price = Column(Float)
    rating = Column(Float)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(String)
    image = Column(String)
    local_image_path = Column(String)
    def __repr__(self):
        return f"<Hotel(name={self.property_title}, city={self.city_name})>"