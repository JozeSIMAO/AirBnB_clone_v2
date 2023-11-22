#!/usr/bin/python3
"""Defines the DBStorage class"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from os import getenv


class DBStorage:
    """A class for database storage using SQLAlchemy"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", default="localhost")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV", default="production")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, database),
                                      pool_pre_ping=True)
        if env == "test":
            print("Dropping tables for testing...")
            Base.metadata.drop_all(self.__engine)
        print("Database initialization complete.")

    def all(self, cls=None):
        """Queries on the current database session"""
        objects = {}
        classes = [User, State, City, Amenity, Place, Review]

        if cls is not None:
            classes = [cls]

        for class_obj in classes:
            query = self.__session.query(class_obj)
            for obj in query.all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj

        return objects

    def new(self, obj):
        """Add the object to the current database session (self.__session)."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session (self.__session)."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session (self.__session) if not None."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the current database
        session from the engine.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """closes the  working alchemy session"""
        self.__session.close()
