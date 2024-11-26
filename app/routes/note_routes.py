from fastapi import APIRouter, HTTPException, Depends
from app.models import Note
from app.database import db
from app.auth import decode_token
from fastapi.security import OAuth2PasswordBearer
import logging  # Import logging for additional debugging
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from bson import ObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# Helper function to get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Decode the JWT token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Extract the user_id from the token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID missing in token")

    # Check if the user exists in the database
    user = db.users.find_one({"user_id": user_id})
    print('After the login ',user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    print('userId:',user_id)

    return user_id


@router.post("/notes/")
async def create_note(note: Note, user_id: str = Depends(get_current_user)):
    print("Inside create_note function")  # Debug 1

    # Associate the note with the current user
    note.user_id = user_id
    print("Current user ID:", user_id)  # Debug 2
    print("Note object before insertion:", note.dict())  # Debug 3

    # Insert the note into the database
    result = db.notes.insert_one(note.dict())
    note_id = result.inserted_id 
    print("Note inserted into database") 
    print(f'Notes id is {note_id}') # Debug 4

    return {"message": "Note created successfully", "note_id": str(note_id)}


@router.put("/notes/{note_id}")
async def update_note(note_id: str, updated_note: Note, user_id: str = Depends(get_current_user)):
    # Check if the note exists and belongs to the user
    existing_note = db.notes.find_one({"_id": ObjectId(note_id), "user_id": user_id})
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Update the note with new data
    updated_data = updated_note.dict()
    updated_data.pop("user_id", None)  # Prevent changing user_id
    db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": updated_data})
    return {"message": "Note updated successfully"}

@router.delete("/notes/{note_id}")
async def delete_note(note_id: str, user_id: str = Depends(get_current_user)):
    # Check if the note exists and belongs to the user
    existing_note = db.notes.find_one({"_id": ObjectId(note_id), "user_id": user_id})
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Delete the note
    db.notes.delete_one({"_id": ObjectId(note_id)})
    return {"message": "Note deleted successfully"}


@router.get("/notes/")
async def view_notes(user_id: str = Depends(get_current_user)):
    # Fetch all notes for the current user
    notes = list(db.notes.find({"user_id": user_id}))
    for note in notes:
        note["_id"] = str(note["_id"])  # Convert ObjectId to string for JSON serialization
    return {"notes": notes}

# Include the router in the app
app.include_router(router)