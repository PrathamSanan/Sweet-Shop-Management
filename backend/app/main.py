from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import auth

# 👇 VERY IMPORTANT
from app.models import user, sweet

app = FastAPI(title="Sweet Shop Management API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/")
def health_check():
    return {"status": "API running"}

from app.routes import sweets

app.include_router(sweets.router)

