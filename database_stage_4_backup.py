from sqlalchemy import create_engine, Column, String, Integer, DateTime
#Import SQLalchemy to work with databases via object-relational mappings and connections
#Import the create_engine module to connect to databases
#Import the Column module to define table columns
#Import the String, Integer, and DateTime modules to specify a column to store strings, specify a column to store numbers, and specify a column to store timestamps

from sqlalchemy.orm import declarative_base
#Import the declarative_base module to create a base class for defining database models, which are tables

from sqlalchemy.orm import sessionmaker, Session
#Import the sessionmaker and Session module to create and manage sessions and interact with the database

import datetime
#Import the datetime library to parse various time formats

import os
#Import the os module to interact with operating systems

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "shortener.db")
DATABASE_URL = "sqlite:///./shortener.db"
#Define the SQLite database URL
#Fix the absolute path to the dabatase in the correct directory

engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})
#Create a database engine

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
#Create a session factory

Base = declarative_base()
#Define the base class for object-relational mapping models

class URLMapping(Base):
    __tablename__ = "URLs"
    the_short_url = Column(String, primary_key = True)
    the_long_url = Column(String, nullable = False)
    the_click_count = Column(Integer, default = 0, nullable = False)
    the_last_click = Column(DateTime, nullable = True)
#Establish a table for URLs containing the long URL name, the short URL name, and the click count
#Set the column for the short URL as the primary key column
#Set 0 as the default, starting number for the click count column
#Collect the time the last click occured
    
def init_database():
    Base.metadata.create_all(bind = engine)
init_database()
#Initialize the database with bind being the engine
#Create the database if it does not already exist