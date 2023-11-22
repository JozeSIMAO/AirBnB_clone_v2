#!/usr/bin/python3
"""This module defines a class User"""
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)  # Column for email
    password = Column(String(128), nullable=False)  # Column for password
    first_name = Column(String(128))  # Column for first name
    last_name = Column(String(128))  # Column for last name
