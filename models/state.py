#!/usr/bin/python3
"""Defines a class State"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv

class State(BaseModel):
    """Represents a State

    Attributes:
        __tablename__(str): Name of the table
        name (str): The name of the state
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City", backref="state",
                          cascade="delete")
    
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            Getter attribute that returns the list of Cities
            (city instances) with a state_id equal to the
            current State.id
            """
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
