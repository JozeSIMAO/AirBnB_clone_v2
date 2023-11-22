#!/usr/bin/python3
""" State Module for HBNB project - Update """

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City  # Assuming City class is defined in city.py

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    
    name = Column(String(128), nullable=False)  # Column for state name (max length 128 characters)
    
    # Relationship for DBStorage: State to City (if State is deleted, all linked City objects are automatically deleted)
    cities = relationship('City', backref='state', cascade='all, delete-orphan')
    
    # Relationship for FileStorage: Getter attribute for cities
    @property
    def cities(self):
        """ Getter attribute for cities in FileStorage """
        from models import storage
        city_list = []
        all_cities = storage.all(City)
        for city in all_cities.values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
