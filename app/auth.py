from jose import JWTError, jwt
from datetime import datetime, timedelta
import secrets
import os
from dotenv import load_dotenv

# Load environment variables (optional: for production, store SECRET_KEY securely in an env file)
load_dotenv()  # This will load .env file if it exists

# Generate a random secret key or fetch it from an environment variable
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))  # Default to random if not found in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Function to create a JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    print('to cncode:',data)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "sub": data['sub']  # Ensure the user_id is included under 'sub'
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to decode a JWT token and get the payload
def decode_token(token: str):
    try:
        print('decode called!!')
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)  # Debug: Print the decoded token
        return payload  # Returns the decoded token if valid
    except JWTError:
        return None  # If decoding fails, return None (invalid or expired token)
