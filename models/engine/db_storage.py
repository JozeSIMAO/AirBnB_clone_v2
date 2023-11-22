from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import User, State, City, Amenity, Place, Review  # Import all classes that inherit from Base

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DBStorage"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.
            format(getenv('HBNB_MYSQL_USER'),
                   getenv('HBNB_MYSQL_PWD'),
                   getenv('HBNB_MYSQL_HOST'),
                   getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

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
        """Adds the object to the current database"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

