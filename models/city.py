#!/usr/bin/python3
"""Defines a class City that inherits from BaseModel"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Represents the City

    Attributes:
        state_id (str): the States ID
        name (str): The name of the city
    """
    __tablename__ = 'cities'

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id', ondelete='CASCADE'),
                      nullable=False)
    places = relationship("Place", backref="cities", cascade="delete")
