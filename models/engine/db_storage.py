#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker, Session
from os import getenv

classes = {'State': State, 'City': City,
           'User': User, 'Place': Place,
           'Review': Review, 'Amenity': Amenity}


class DBStorage:
    """This class manages storage of hbnb models in JSON format"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates SQLAlchemy engine"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        temp = {}
        if cls == None:
            for v in classes.values():
                for instance in self.__session.query(v):
                    key = "{}.{}".format(type(instance).__name__, instance.id)
                    temp[key] = instance
        else:
            if type(cls) is str:
                cls = eval(cls)
            for instance in self.__session.query(cls):
                key = "{}.{}".format(type(cls).__name__, instance.id)
                temp[key] = instance
        return temp

    def new(self, obj):
        """Adds new object to storage database"""
        self.__session.add(obj)

    def save(self):
        """Commits to the current database session"""
        self.__session.commit()

    def reload(self):
        """Creates a new database session"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)

    def delete(self, obj=None):
        if obj == None:
            pass
        else:
            cls = classes[type(obj).__name__]
            self.__session.query(cls).filter(cl.id == obj.id).delete()

    def close(self):
        """Close scoped session"""
        self.__session.remove()
