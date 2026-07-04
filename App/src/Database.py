import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import os

db_address = os.environ.get("DATABASE_HOST")
db_port = int(os.environ.get("DATABASE_PORT"))
db_password = os.environ.get("DATABASE_PASSWORD")
db_name = os.environ.get("DATABASE_NAME")

engine = sa.create_engine(f"postgresql://postgres:{db_password}@{db_address}:{db_port}/{db_name}")
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()