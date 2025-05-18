from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_XHsdqxKLP1t7@ep-misty-scene-a187pyvj-pooler.ap-southeast-1.aws.neon.tech/neondb?ssl=require"

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    echo = False,
    future =  True
)

async_session = sessionmaker(
    bind = engine,
    expire_on_commit = False,
    class_ = AsyncSession
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)