from sqlalchemy import create_engine, Column, String, Integer
#Import SQLalchemy to work with databases via object-relational mappings and connections
#Import the create_engine module to connect to databases
#Import the Column, String, and Integer modules to define table columns, specify a column to store strings, and specify a column to store numbers

from sqlalchemy.ext.declarative import declarative_base
#Import the declarative_base module to create a base class for defining database models, which are tables

from sqlalchemy.orm import sessionmaker, Session
#Import the sessionmaker and Session module to create and manage sessions and interact with the database

DATABASE_URL = "sqlite:///./shortener.db"
#Define the SQLite database URL

engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})
#Create a database engine

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
#Create a session factory

Base = declarative_base()
#Define the base class for object-relational mapping models

class URLMapping(Base):
    __tablename__ = "URLs"
    the_short_url = Column(String, primary_key = True)
    the_long_url = Column(String)
    the_click_count = Column(Integer, default = 0)
#Establish a table for URLs containing the long URL name, the short URL name, and the click count
#Set the column for the short URL as the primary key column
#Set 0 as the default, starting number for the click count column

def init_database():
    Base.metadata.create_all(bind = engine)
init_database()
#Initialize the database with bind being the engine
#Create the database if it does not already exist