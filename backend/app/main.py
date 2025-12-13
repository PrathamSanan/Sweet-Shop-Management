from fastapi import FastAPI

app = FastAPI(title="Sweet Shop Management API")

@app.get("/")
def health_check():
    return {"status": "API running"}
