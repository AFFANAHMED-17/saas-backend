from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Handle SSL arguments for cloud databases (Render, etc.)
connect_args = {}
if "ssl" in settings.DATABASE_URL:
     # Basic SSL context to satisfy providers like Render/Planetcale if needed
     # Often just {"ssl": {"ca_path": ...}} or similar is needed.
     # But if the error is "str object has no attribute get", it implies 'ssl' IS a string.
     pass

engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True,
    # connect_args=connect_args # Only add if we construct it manually
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
