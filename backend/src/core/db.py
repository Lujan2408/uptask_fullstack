# Database async connection
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.config import settings
from fastapi import Depends
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from colorama import Fore, Style

# from src.models import *

# Create async engine
async_engine = create_async_engine(
  settings.SQLALCHEMY_ASYNC_DATABASE_URI,
  echo=True,
  future=True,
)

# Create async session 
AsyncSessionLocal = async_sessionmaker(
  async_engine,
  class_=AsyncSession,
  expire_on_commit=False,
)

async def create_db_and_tables():
  async with async_engine.begin() as connection: 
    await connection.run_sync(SQLModel.metadata.create_all)
    print(Fore.GREEN + "Successfully connected to database ✅" + Style.RESET_ALL)

@asynccontextmanager
async def lifespan(app): 
  await create_db_and_tables()
  yield

async def get_async_session() -> AsyncGenerator[AsyncSession, None]: 
  async with AsyncSessionLocal() as session: 
    try: 
      yield session
    finally: 
      await session.close() 

AsyncSessionDependency = Annotated[AsyncSession, Depends(get_async_session)]