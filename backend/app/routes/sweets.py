from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.sweet import Sweet
from app.schemas.sweet import SweetCreate

router = APIRouter(prefix="/api/sweets", tags=["Sweets"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_sweet(sweet: SweetCreate, db: Session = Depends(get_db)):
    new_sweet = Sweet(**sweet.dict())
    db.add(new_sweet)
    db.commit()
    db.refresh(new_sweet)
    return new_sweet

@router.get("/")
def list_sweets(db: Session = Depends(get_db)):
    return db.query(Sweet).all()
