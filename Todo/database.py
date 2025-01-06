from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Create db URL
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todo.db'
#Create Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
#Create local Session
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)
#Create Model structure
Base = declarative_base()