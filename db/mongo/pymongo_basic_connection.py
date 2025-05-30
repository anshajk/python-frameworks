from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import certifi


connection_string = os.getenv("MONGODB_URI")


client = MongoClient(
    connection_string, server_api=ServerApi("1"), tlsCAFile=certifi.where()
)


client.admin.command("ping")
print("Successfully connected to MongoDB Atlas!")


db = client["sample_mflix"]
collection = db["movies"]

val = collection.count_documents({"year": {"$gte": 2000}})
print(val)


for movie in collection.find({"directors": "Christopher Nolan"}):
    print(movie)
