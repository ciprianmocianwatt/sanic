from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config import Base


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(ForeignKey("user.id"))

    def __repr__(self):
        return f'Article {self.title}'


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    article = relationship("Article", backref="article")
    email_histories = relationship("UserEmailHistory", backref="user")
    addresses = relationship("Address", backref="user")


class UserEmailHistory(Base):
    __tablename__ = 'user_email_history'

    id = Column(Integer, primary_key=True)
    user_email = Column(String)
    user_id = Column(ForeignKey("user.id"))


class Magazine(Base):
    __tablename__ = "magazine"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    street = Column(String)
    postcode = Column(String)
    number = Column(Integer)
    user_id = Column(ForeignKey("user.id"))
