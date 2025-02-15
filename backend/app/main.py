import sys
import os
from fastapi import FastAPI

# Ensure the correct module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from fastapi import FastAPI
from app.routes import users, auth
from database import engine, Base

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AirFluence API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
