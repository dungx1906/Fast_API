from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

URL_DATABASE = "mysql+pymysql://root:123456@localhost:3306/restaurant_db"

engine = create_engine(URL_DATABASE)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = sessionLocal
    try:
        yield db

    finally:
        
        db.close()