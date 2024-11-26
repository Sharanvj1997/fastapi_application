from fastapi import FastAPI, APIRouter, HTTPException, Depends
from app.models import User, Note
from app.database import db
from app.auth import create_access_token, decode_token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# Create the router, app, and password context
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# # Helper function to get current user from token
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     # Decode the JWT token
#     payload = decode_token(token)
#     if not payload:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     # Extract the user_id from the token
#     user_id = payload.get("sub")
#     if not user_id:
#         raise HTTPException(status_code=401, detail="User ID missing in token")

#     # Check if the user exists in the database
#     user = db.users.find_one({"user_id": user_id})
#     print('After the login ',user)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     print('userId:',user_id)

#     return user_id

# User Registration Endpoint
@router.post("/register/")
async def register_user(user: User):
    if db.users.find_one({"user_email": user.user_email}):
        raise HTTPException(status_code=400, detail="Email already in use")
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    db.users.insert_one(user.dict())
    return {"message": "User registered successfully"}

# User Login Endpoint
@router.post("/login/")
async def login(email: str, password: str):
    user = db.users.find_one({"user_email": email})
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["user_id"]})
    return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/notes/")
# async def create_note(note: Note, user_id: str = Depends(get_current_user)):
#     print("Inside create_note function")  # Debug 1

#     # Associate the note with the current user
#     note.user_id = user_id
#     print("Current user ID:", user_id)  # Debug 2
#     print("Note object before insertion:", note.dict())  # Debug 3

#     # Insert the note into the database
#     db.notes.insert_one(note.dict())
#     print("Note inserted into database")  # Debug 4

#     return {"message": "Note created successfully"}


# Include the router in the app
app.include_router(router)
