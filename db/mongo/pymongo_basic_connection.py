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

total_documents = collection.count_documents({})
print(f"Total documents: {total_documents}")


nolan_movies = []

for movie in collection.find({"directors": "Christopher Nolan"}):
    nolan_movies.append(movie)


print("Nolan Movies")

print(nolan_movies)

for movie in nolan_movies:
    print(movie["title"])
