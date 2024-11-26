from fastapi import FastAPI
from app.routes import user_routes, note_routes

app = FastAPI()

# Include routes
app.include_router(user_routes.router)
app.include_router(note_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Backend Assignment API"}
