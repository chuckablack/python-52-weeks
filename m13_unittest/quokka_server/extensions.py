from pymongo import MongoClient
import os
from pprint import pprint

client = MongoClient()
if "TESTDB" not in os.environ:
    db = client.quokkadb
else:
    client.drop_database("testdb")
    db = client.testdb
