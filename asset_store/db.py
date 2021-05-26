from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_session():
    engine = create_engine('sqlite:///database/db.db')
    session = sessionmaker(bind=engine)()
    return session
