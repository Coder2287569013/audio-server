from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase): pass

class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True

class MusicBase(BaseModel):
    name: str
    author_id: int

class MusicCreate(MusicBase): pass

class Music(MusicBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    login: str
    password: str

class UserCreate(UserBase): pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class PlaylistBase(BaseModel):
    user_name: str
    music_name: str

class PlaylistCreate(PlaylistBase): pass

class Playlist(PlaylistBase):
    id: int
    class Config:
        from_attributes = True