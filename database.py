from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import settings

engine = create_engine(url=settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()
