from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from utils.db.base import Base

import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is unknown.")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=2,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10,
    },
)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
