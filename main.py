from fastapi import FastAPI, Path, Query, File, UploadFile, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from typing_extensions import Annotated

from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.engine import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.mount("/sound", StaticFiles(directory = "sound"), name = "sound")
app.mount("/img", StaticFiles(directory = "img"), name = "img")
app.mount("/css", StaticFiles(directory = "css"), name = "css")
templates = Jinja2Templates(directory = "templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def get_list_sounds(request: Request, db: Session = Depends(get_db)):
    data = {"list": crud.get_musics(db=db)}

    return templates.TemplateResponse("index.html", {"request": request, "data": data})

@app.get("/author/get-all")
async def get_all_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db=db)

@app.get("/audio-sounds/{sound}/")
async def get_sound_info(request: Request, 
                         sound: Annotated[str, Path(
                                min_length = 5, 
                                max_length = 50, 
                                description = "Getting the information about the file by using it's name")], 
                        db: Session = Depends(get_db)):
    music = crud.get_music(db=db, name=sound)
    data = {"name": music.name}

    return templates.TemplateResponse("sound-page.html", {"request": request, "data": data})

# @app.get("/user/get-all/")
# async def get_all_users(db: Session = Depends(get_db)):
#     return crud.get_users(db=db)

@app.get("/playlist/get/")
async def get_playlist(request: Request, user_name: str, db: Session = Depends(get_db)):
    data = {"list": crud.get_playlist(db=db, user_name=user_name), "username": user_name}
    return templates.TemplateResponse("playlist-page.html", {"request": request, "data": data})

@app.get("/user/get-all")
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

@app.post("/audio-sounds/upload/")
async def upload_sound(token: Annotated[str, Depends(oauth2_scheme)], author_id: int, file: UploadFile = File(...), db = Depends(get_db)):
    crud.create_music(db=db, file=file, author_id=author_id)

@app.post("/author/create/", response_model=schemas.Author)
def create_author(token: Annotated[str, Depends(oauth2_scheme)], author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.post("/user/create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/playlist/create/", response_model=schemas.Playlist)
def create_playlist(token: Annotated[str, Depends(oauth2_scheme)], playlist: schemas.PlaylistCreate, db: Session = Depends(get_db)):
    if user.login == playlist.user_name:
        return crud.create_playlist(db=db, playlist=playlist)
    else:
        raise HTTPException(status_code=400, detail="Cannot add a sound to another user's playlist!")

@app.delete("/audio-sounds/delete/{filename}/")
async def delete_sound(token: Annotated[str, Depends(oauth2_scheme)],
                       filename: Annotated[str, Path(
                                min_length = 5, 
                                max_length = 50, 
                                description = "Searching for the file by it's name")],
                       db: Session = Depends(get_db)):
    crud.delete_music(db=db, filename=filename)

@app.delete("/playlist/delete")
async def delete_playlist(token: Annotated[str, Depends(oauth2_scheme)],user_name: str, music_name: str, db: Session = Depends(get_db)):
    if user.login == user_name:
        return crud.delete_playlist(db=db, user_name=user_name, music_name=music_name)
    else:
        raise HTTPException(status_code=400, detail="Cannot delete a sound from another user's playlist!")
    
@app.post("/token")
async def token_create(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user_data = crud.get_user(db=db, login=form_data.username)
    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect username of password!")
    
    global user
    user = schemas.UserBase(login=user_data.login, password=user_data.password)
