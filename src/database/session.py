from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from src.database.engine import engine





SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()