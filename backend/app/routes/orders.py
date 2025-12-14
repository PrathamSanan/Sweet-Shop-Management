from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.deps import get_current_user, get_admin_user
from app.models.order import Order

router = APIRouter(prefix="/api/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# USER ORDERS
@router.get("/my")
def my_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Order).filter(Order.user_id == user.id).all()

# ADMIN: ALL ORDERS
@router.get("/")
def all_orders(
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    return db.query(Order).all()
