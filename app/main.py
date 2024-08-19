from .schemas import SongCreate, EmailRequest, ScrapeRequest
from .database import engine, Base, async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, BackgroundTasks
from .utils import send_email, validate_url
from fastapi import HTTPException, status
from sqlalchemy.future import select
from .models import Song
from typing import List
from . import crud

app = FastAPI()

# Criando as tabelas de forma assíncrona
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_models()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/songs/", response_model=Song)
async def create_song(song: SongCreate):
    async with async_session() as session:
        db_song = Song.from_orm(song)
        session.add(db_song)
        await session.commit()
        await session.refresh(db_song)
        return db_song

@app.get("/songs/", response_model=List[Song])
async def read_songs():
    async with async_session() as session:
        result = await session.execute(select(Song))
        songs = result.scalars().all()
        return songs

@app.post("/send-email/")
async def send_email_endpoint(request: EmailRequest, background_tasks: BackgroundTasks):
    # Adiciona a tarefa de enviar e-mail em segundo plano
    background_tasks.add_task(send_email, request.email, request.subject, request.message)
    return {"message": "Email is being sent in the background"}
    
@app.post("/scrape/")
async def scrape_endpoint(request: ScrapeRequest, background_tasks: BackgroundTasks):
    url = request.url
    
    # Valida o formato da URL
    if not validate_url(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL format")
    
    async with async_session() as session:
        # Inicia a tarefa em segundo plano
        background_tasks.add_task(crud.scrape_and_store, url, session)
    
    return {"message": "Scraping started in the background"}

@app.get("/scraped-data/")
async def read_scraped_data():
    async with async_session() as session:
        data = await crud.read_scraped_data(session)
        return data