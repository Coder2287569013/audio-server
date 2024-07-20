from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from .engine import Base

class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

class DBMusic(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True, index=True)   
    name = Column(String(50), nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor)

class DBUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)  
    login = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

class DBPlaylist(Base):
    __tablename__ = "playlist"

    id = Column(Integer, primary_key=True, index=True)
    music_name = Column(String(255), ForeignKey("music.name"))
    user_name = Column(Integer, ForeignKey("user.login"))

    music = relationship(DBMusic)
    user = relationship(DBUser)
