from fastapi import FastAPI
from app.core.database import engine, Base

# IMPORTANT: models import so tables create ho
from app.models import user, sweet

# Routers
from app.routes import auth, sweets

app = FastAPI(title="Sweet Shop Management API")

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(sweets.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
