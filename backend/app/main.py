from fastapi import FastAPI
from app.core.database import engine, Base

app = FastAPI(title="Sweet Shop Management API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "API running"}
