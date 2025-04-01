from fastapi import FastAPI, HTTPException, Depends
#Import the FastAPI web framework for building high-performance Fast APIs
#Import HTTPException to allow HTTP error messages to be sent
#Import Depends for dependency injection for automatically managing database connections

from fastapi.responses import JSONResponse, RedirectResponse
#Import the RedirectResponse module to redirect the new short URL to the same place as the old long URL

from sqlalchemy import create_engine, Column, String
#Import SQLalchemy to work with databases via object-relational mappings and connections
#Import the create_engine module to connect to databases
#Import the Column and String modules to define table columns and specify a column to store strings

from sqlalchemy.ext.declarative import declarative_base
#Import the declarative_base module to create a base class for defining database models, which are tables

from sqlalchemy.orm import sessionmaker, Session
#Import the sessionmaker and Session module to create and manage sessions and interact with the database

import random, string
#Import the random and string modules to generate random numbers and contain predefined character sets

import os
#Import the os module to interact with operating systems

import json
#Import JSON to make sure the proper format is used

from pydantic import BaseModel
#Import the BaseModel module to help validate the request contains expected data type and is properly structured

import logging
#Import logging to help with debugging issues

from urllib.parse import unquote
#Import the unquote module from urllib to parse URLs correctly

from database import SessionLocal, URLMapping
#Import the SessionLocal and URLMapping modules for database management

from datetime import datetime
#Import the datetime library to parse various time formats

app = FastAPI()

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Establish the dependency to get a database session

@app.get("/")
def home():
    return{"message": "Hello and welcome, you are now at the API for Project Link Shortener."}
#Initiate the FastAPI app and setup the testing-purpose root route

"""def load_url_database():
        try:
            with open("url_database.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}"""
#Load URLs from a JSON file

"""def save_url_database(data):
        with open("url_database.json", "w") as file:
            json.dump(data, file)
            print("Saved to JSON file:", data)"""
#Save URLs to a JSON file

"""url_database = load_url_database()"""
#Set up a place for the storage of URLs for later use

class Request_URL(BaseModel):
    old_long_url: str
#Set up for validation

class Update_URL_Request(BaseModel):
    new_long_url: str
#Set up URL updating

def shortened_url_generator(total_length = 8):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k = total_length))
#Set up a function to generate a shortened URL with a length of 8 based on ASCII letters and digits
#Form a 62-character alphanumeric set, namely 26 upper case letters, 26 lower case letters, and 10 digits

"""@app.post("/shorten_url")
    def url_shortening(request: Request_URL):
        new_short_url = shortened_url_generator()
        old_long_url = request.old_long_url.strip()
        if not old_long_url.startswith(("http://", "https://")):
            old_long_url = "http://" + old_long_url
        url_database[new_short_url] = old_long_url
        save_url_database(url_database)
        print("Database Contents:", url_database)
        return{"new_short_url": new_short_url, "old_long_url": old_long_url}"""
#Define a function to generate a new short URL from an old long URL
#Insert the new URL into the URL database
#Discarded but kept to document the original core functionality design

@app.post("/shorten_url")
def url_shortening(request: Request_URL, db: Session = Depends(get_database)):
    new_short_url = shortened_url_generator()
    old_long_url = request.old_long_url.strip()
    if not old_long_url.startswith(("http://", "https://")):
        old_long_url = "http://" + old_long_url
    database_url = URLMapping(the_short_url = new_short_url, the_long_url = old_long_url)
    db.add(database_url)
    db.commit()
    return{"new_short_url": new_short_url, "old_long_url": old_long_url}
#Define a function to generate a new short URL from an old long URL
#Insert the new URL into the URL SQLite database

@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(status_code = 204, content = None)
#Prevent unnecessary 404 logs in the FastAPI server

"""@app.get("/{new_short_url}")
    def redirect_url(new_short_url: str):
        url_database = load_url_database()
        new_short_url = unquote(new_short_url)
        print(f"Incoming Request For: ", repr(new_short_url))
        print(f"JSON Database Contents: ", url_database)
        if new_short_url in url_database:
            old_long_url = url_database[new_short_url]
            print(f"FOUND: Redirecting to {old_long_url}")
            return RedirectResponse(url = old_long_url, status_code = 308)  
        else:
            print(f"ERROR: '{new_short_url}' NOT FOUND in database!")
            raise HTTPException(status_code = 404, detail = "Sorry, URL Not Found!")"""
#Redirect permanently to prevent recursive requests
#Establish corresponding error messages

@app.get("/short/{new_short_url}") 
def redirect_url(new_short_url: str, db: Session = Depends(get_database)):
    decoded_url = unquote(new_short_url)  # Decoding potential URL-encoded input
    
    url_entry = db.query(URLMapping).filter(URLMapping.the_short_url == decoded_url).first()
    
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found!")

    url_entry.the_click_count += 1
    url_entry.the_last_click = datetime.utcnow()  # Ensure datetime is imported correctly
    
    db.commit()  # Save updates to the database

    return RedirectResponse(url=url_entry.the_long_url, status_code=308)


@app.get("/list_of_urls")
def list_all_urls(db: Session = Depends(get_database)):
    print("The list_all_urls function is called!")
    urls = db.query(URLMapping).all()
    print(f"Raw URls from database: {urls}")
    if not urls:
        print("No URLs found in DB, returning 404!")
        raise HTTPException(status_code = 404, detail = "No URLs found!")
    print("URLs found, returning data.ta")
    return urls

@app.delete("/delete_url/{delete_short_url}")
def delete_url(delete_short_url: str, db: Session = Depends(get_database)):
    print(f"Attempting to delete: {delete_short_url}")
    url_entry = db.query(URLMapping).filter(URLMapping.the_short_url == delete_short_url).first()
    if not url_entry:
        raise HTTPException(status_code = 404, detail = "Short URL not found!")
    db.delete(url_entry)
    db.commit()
    return{"message": f"Short URL {delete_short_url} deleted successfully."}