from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    # name = Column(String(100))
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(32))
    picture = Column(String(250))
    password_hash = Column(String(64))
    # create_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    # update_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'picture': self.picture
            # 'create_date': self.create_date,
            # 'update_date': self.update_date
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    # create_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    # update_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            # 'create_date': self.create_date,
            # 'update_date': self.update_date,
            'user_id': self.user_id
        }


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    author = Column(String(100))
    # create_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    # update_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            # 'create_date': self.create_date,
            # 'update_date': self.update_date,
            'category_id': self.category_id,
            'user_id': self.user_id
        }


engine = create_engine('sqlite:///category.db')


Base.metadata.create_all(engine)
