import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String


class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(String)
    user = Column(String)
    text = Column(String)
    color = Column(String)

engine = create_async_engine(
    "postgresql+asyncpg://postgres:your",
    echo=True
)


SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_message(text, user=None, color=None, chat_id=None):
    async with SessionLocal() as session:
        session.add(Message(text=text, user=user, color=color, chat_id=chat_id,))
        await session.commit()


async def main():
    await init_db()

if __name__ == "__main__":
    asyncio.run(main())
