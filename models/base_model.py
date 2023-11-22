#!/usr/bin/python3
"""Defines a class BaseModel"""
import models
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """
    BaseModel represents a basic model with common attributes and methods.
    Public instance attributes:
    - id (str): A unique identifier for the object.
    - created_at (datetime): The timestamp when the object was created.
    - updated_at (datetime): The timestamp of the last update.

    Public instance methods:
    - save(): Updates the 'updated_at' timestamp to the current time.
    - to_dict(): Converts the object to a dictionary with specific formatting.
    - __str__(): Returns a str representation of the obj in a specific format.
    """
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initialize a new BaseModel object with unique ID and timestamps.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments for object initialization.
        """
        timeformat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        value = datetime.strptime(value, timeformat)
                    setattr(self, key, value)
        else:
            models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the object

        Returns:
            str: A string representation of the object in a specific format
        """
        classname = self.__class__.__name__
        return "[{}] ({}) {}".format(classname, self.id, self.__dict__)

    def save(self):
        """
        Update the 'updated_at' timestamp to the current time and
        save the object.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Convert the object to a dictionary.

        Returns:
            dict: A dict representation of the object with specific formatting.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict.pop('_sa_instance_state', None)
        return obj_dict
