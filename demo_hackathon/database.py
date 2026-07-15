from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/Vehicle_db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

sessionlocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = sessionlocal()
    try:
        yield db

    finally:
        db.close()