"""
Database main config
"""
import os
from .mongodb_client import MongoDBClient
from .mongodb_database import MongoDBDatabase
from .mongodb_collections import MongoDBCollections
from .constants import DATABASE_NAME
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

PASSWORD = os.environ.get("MONGODB_PWD")

USER = os.environ.get("MONGODB_USER")

CONN_STRING = f'mongodb+srv://{USER}:{PASSWORD}@mycluster.nm13zpf.mongodb.net/?retryWrites=true&w=majority'

mongoDBClient = MongoDBClient(CONN_STRING)

mongoDBDatabase = MongoDBDatabase(mongoDBClient.client, DATABASE_NAME)

DB = MongoDBCollections(mongoDBDatabase.database)
