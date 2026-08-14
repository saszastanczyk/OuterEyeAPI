from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine
import os

db_address = os.environ.get("DATABASE_HOST")
db_port = int(os.environ.get("DATABASE_PORT"))
db_password = os.environ.get("DATABASE_PASSWORD")
db_name = os.environ.get("DATABASE_NAME")

engine = create_async_engine(f"postgresql+asyncpg://postgres:{db_password}@{db_address}:{db_port}/{db_name}",pool_size=10,pool_pre_ping=True)
LocalSession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db():
    db =  LocalSession()
    try:
        yield db
    finally:
        await db.close()