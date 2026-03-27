import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env файлы бар болса, соның ішіндегіні оқиды
load_dotenv()

# Render берген DATABASE_URL сілтемесін алады. Егер ол жоқ болса (локалды компьютерде), SQLite қолданады.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unichance.db")

# Render-дегі PostgreSQL кейде "postgres://" деп басталады, SQLAlchemy оны "postgresql://" деп қабылдауы үшін түзетеміз
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Егер SQLite болса "check_same_thread": False керек, ал Postgres болса керек емес
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()