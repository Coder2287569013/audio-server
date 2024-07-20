from sqlalchemy.orm import Session
from db import schemas, models
import os

def get_authors(db: Session):
    return db.query(models.DBAuthor).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name = author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_musics(db: Session):
    return [music.name for music in db.query(models.DBMusic).all()]

def get_music(db: Session, name: str):
    return db.query(models.DBMusic).filter(models.DBMusic.name.contains(name)).first()

def delete_music(db: Session, filename: str):
    music = get_music(db=db, name=filename)
    db.query(models.DBMusic).filter(models.DBMusic.name == music.name).delete()
    db.commit()
    file_path = f"sound/{music.name}"
    print(file_path)
    os.remove(file_path)

def create_music(db: Session, file, author_id: int):
    try:
        if 5 <= len(file.filename) <= 50: 
            file_path = f"sound/{file.filename}"
            with open(file_path, "wb+") as f:
                f.write(file.file.read())
            db_music = models.DBMusic(name=file.filename, author_id=author_id)
            db.add(db_music)
            db.commit()
            db.refresh(db_music)
            
    except Exception:
        return {"message": "Cannot upload"}
    
    finally:
        file.file.close()

def get_users(db: Session):
    return db.query(models.DBUser).all()

def get_user(db: Session, login: str):
    return db.query(models.DBUser).filter(models.DBUser.login == login).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.DBUser(login = user.login, password = user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_playlist(db: Session, user_name: str):
    data = db.query(models.DBPlaylist.music_name).filter(models.DBPlaylist.user_name == user_name).all()
    playlist_data = [data[i][0] for i in range(len(data))]
    return playlist_data

def delete_playlist(db: Session, user_name: str, music_name: str):
    db.query(models.DBPlaylist).filter(models.DBPlaylist.user_name == user_name, models.DBPlaylist.music_name.contains(music_name)).delete()
    db.commit()

def create_playlist(db: Session, playlist: schemas.PlaylistCreate):
    db_playlist = models.DBPlaylist(music_name = playlist.music_name, user_name = playlist.user_name)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)

    return db_playlist