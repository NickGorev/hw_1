from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

parser = ConfigParser()
parser.read("database.ini")

DB_HOST = parser["postgresql"]["hostname"]
DB_PORT = parser["postgresql"]["port"]
DB_NAME = parser["postgresql"]["database"]
DB_USER = parser["postgresql"]["username"]
DB_PASSWORD = parser["postgresql"]["password"]

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
