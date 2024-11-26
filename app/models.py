from pydantic import BaseModel, EmailStr
from uuid import uuid4
from datetime import datetime

class User(BaseModel):
    user_id: str = str(uuid4())
    user_name: str
    user_email: EmailStr
    mobile_number: str
    password: str
    last_update: datetime = datetime.utcnow()
    created_on: datetime = datetime.utcnow()

from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4

class Note(BaseModel):
    note_id: str = str(uuid4())  # Automatically generated
    note_title: str
    note_content: str
    user_id: str = None  # Populated in `create_note`, not in the request
    last_update: datetime = datetime.utcnow()
    created_on: datetime = datetime.utcnow()


