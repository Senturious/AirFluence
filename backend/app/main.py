import sys
import os
from fastapi import FastAPI

# Ensure the correct module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from fastapi import FastAPI
from app.routes import users, auth
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows for adding specific domains, ex. ["http://localhost:4000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS itd.)
    allow_headers=["*"],  # Allows for all headers
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes with prefixes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AirFluence API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
