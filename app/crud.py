from .utils import model_to_dict, scrape_website
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict
from sqlalchemy.future import select
from .database import async_session
from .models import ScrapedData

async def store_scraped_data(data: Dict[str, Optional[List[str]]], session: AsyncSession):
    try:
        async with async_session() as session:
            scraped_data = ScrapedData(
                title=data['title'],
                meta_description=data.get('meta_description'),
                headings=data.get('headings', []),  # Armazena diretamente como lista
                links=data.get('links', []),        # Armazena diretamente como lista
                content=data.get('content', [])     # Armazena diretamente como lista
            )

            session.add(scraped_data)
            await session.commit()
            await session.refresh(scraped_data)

            print("Data stored successfully")

    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")
        await session.rollback()
    except Exception as e:
        print(f"Error while storing data: {e}")
        await session.rollback()

async def scrape_and_store(url: str, session: AsyncSession):
    try:
        data = scrape_website(url)
        await store_scraped_data(data, session)
    except Exception as e:
        # Adiciona tratamento de exceção adequado
        print(f"Error while scraping and storing data: {e}")

async def read_scraped_data(session: AsyncSession) -> List[Dict[str, Optional[str]]]:
    result = await session.execute(select(ScrapedData))
    scraped_data = result.scalars().all()

    return [
        {
            "id": data.id,
            "title": data.title,
            "meta_description": data.meta_description,
            "headings": data.headings,
            "links": data.links,       
            "content": data.content  
        }
        for data in scraped_data
    ]