#!/usr/bin/python3
"""
DBStorage class for PostgreSQL
"""

import models
from config.settings import Config
from models.base import Base
from models.models import User, Product, Order, OrderItem, Category, Review, Cart, CartItem
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Add all models to this dictionary
classes = {
    "User": User,
    "Product": Product,
    "Order": Order,
    "OrderItem": OrderItem,
    "Category": Category,
    "Review": Review,
    "Cart": Cart,
    "CartItem": CartItem,
}

class DBStorage:
    """Interacts with the PostgreSQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""

        self.__engine = create_engine(Config.POSTGRESQL_DATABASE_URI)

        # Drop tables if in test mode
        if Config.SEASE_ENV == "test":
            Base.metadata.drop_all(self.__engine)



    def all(self, cls=None, category=None, **kwargs):
        """Query all objects of a certain class or all classes"""
        category_id = None
        if category:
            categories = self.__session.query(Category).all()
            category_id = [c.id for c in categories if c.name == category]

            if len(category_id) > 0:
                category_id = category_id[0]

        if kwargs:
            o_key = list(kwargs.items())[0][0]
        else:
            o_key = None

        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    if category_id:
                        if hasattr(obj, 'category_id'):
                            if obj.category_id == category_id:
                                new_dict[key] = obj

                    elif o_key == 'cart_id':
                        if hasattr(obj, 'cart_id'):
                            if obj.cart_id == kwargs.get(o_key):
                                new_dict[key] = obj
                    elif o_key == 'user_id':
                        if hasattr(obj, 'user_id'):
                            if obj.user_id == kwargs.get(o_key):
                                new_dict[key] = obj
                    else:
                        new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add object to the current session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the session if provided"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize the session"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Close the current session"""
        self.__session.remove()

    def get(self, cls, **kwargs):
        """Get an object by class and id"""
        if cls not in classes.values():
            return None

        key = list(kwargs.items())[0][0]
        all_cls = models.storage.all(cls)


        for value in all_cls.values():

            if key == 'id':
                if value.id == kwargs.get(key):
                    return value
            elif key == 'name':
                if value.name == kwargs.get(key):
                    return value
            elif key == 'user_id':
                if value.user_id == kwargs.get(key):
                    return value
            elif key == 'product_id':
                if value.product_id == kwargs.get(key):
                    return value
            else:
                if value.email == kwargs.get(key):
                    return value
        return None

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if not cls:
            count = sum(len(models.storage.all(c).values()) for c in classes.values())
        else:
            count = len(models.storage.all(cls).values())
        return count
