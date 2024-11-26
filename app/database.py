from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.user_notes_db

# Query users collection
users = db.users.find()

db.users.delete_many({})
db.notes.delete_many({})
print("Users:")
for user in users:
    print(user)

# Query notes collection
notes = db.notes.find()
print("Notes:")
for note in notes:
    print(note)
