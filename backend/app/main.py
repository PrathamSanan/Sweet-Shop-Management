from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import auth

app = FastAPI(title="Sweet Shop Management API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/")
def health_check():
    return {"status": "API running"}
