#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel, Base
import models


class Place(BaseModel, Base):
    """
    Represents a Place for a MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table places.

    Attributes:
        __tablename__ (str): The name of the MySQL
                            table to store places.
        id (sqlalchemy String): The unique identifier for the place.
        name (sqlalchemy String): The name of the place.
        description (sqlalchemy String): A detailed description of the place.
        number_rooms (sqlalchemy Integer): The
                        number of rooms available.
        number_bathrooms (sqlalchemy Integer): The number
                            of bathrooms in the place.
        max_guest (sqlalchemy Integer): The maximum number of
                            guests the place can accommodate.
        price_by_night (sqlalchemy Integer): The cost per
                            night to stay at the place.
        latitude (sqlalchemy Float): The latitude coordinate of the place.
        longitude (sqlalchemy Float): The longitude coordinate of the place.
        city_id (sqlalchemy String): The ID of the
                            city where the place is located.
        user_id (sqlalchemy String): The ID of the
                            user who owns the place.
        reviews (sqlalchemy relationship): The Place-Review
                            relationship.
        amenities (sqlalchemy relationship): The
                            Place-Amenity relationship.
        amenity_ids (list): A list of IDs of linked amenities.
    """
    __tablename__ = "places"

    id = Column(String(60),
                nullable=False, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    city_id = Column(String(60),
                     ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60),
                     ForeignKey("users.id"), nullable=False)

    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity",
                             secondary="place_amenity", viewonly=False)

    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Get a list of all linked Reviews."""
            return [review for review in models.storage.all(Review).
                    values() if review.place_id == self.id]

        @property
        def amenities(self):
            """Get/set linked Amenities."""
            return [amenity for amenity in models.storage.all(Amenity).
                    values() if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, value):
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
