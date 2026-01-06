import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGO_URL = os.getenv("MONGODB_URI")
print(MONGO_URL)
print("Connecting to MongoDB...")
client = MongoClient(MONGO_URL)

print("Connected to MongoDB.")
db = client["LearningLog"]
logs_collection = db["Logs"]