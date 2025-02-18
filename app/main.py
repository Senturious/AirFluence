from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models.key import Key
from app.models.user import User
from app.routers import auth, devices, orders  # Upewnij się, że ten import odpowiada plikom

# Tworzenie aplikacji
app = FastAPI()

# Tworzymy wszystkie tabele w bazie danych
Base.metadata.create_all(bind=engine)

# Konfiguracja middleware (opcjonalnie możesz dostosować do swoich potrzeb)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dla dev możesz użyć "*", w prod ogranicz do domeny frontendowej
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rejestrowanie routerów w głównej aplikacji
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(devices.router, prefix="/devices", tags=["Devices"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])


# Testowy endpoint
@app.get("/")
def health_check():
    return {"message": "Welcome to AirFluence API!"}

