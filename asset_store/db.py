import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.environ["SQLITE_URL"]


def get_db_session():
    engine = create_engine(DATABASE_URL)
    session = sessionmaker(bind=engine)()
    return session
