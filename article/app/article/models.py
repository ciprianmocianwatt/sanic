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
    email_history = relationship("UserEmailHistory", backref="user")


class UserEmailHistory(Base):
    __tablename__ = 'user_email_history'

    id = Column(Integer, primary_key=True)
    user_email = Column(String)
    user_id = Column(ForeignKey("user.id"))


class Magazine(Base):
    __tablename__ = "magazine"

    id = Column(Integer, primary_key=True)
    name = Column(String)
