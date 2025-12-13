from fastapi import APIRouter, status

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register():
    return {"message": "User registered"}
