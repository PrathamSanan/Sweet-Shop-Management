from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.deps import get_current_user, get_admin_user
from app.models.sweet import Sweet
from app.schemas.sweet import SweetUpdate
from app.models.order import Order


router = APIRouter(prefix="/api/sweets", tags=["Sweets"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔓 GET (login required)
@router.get("/")
def get_sweets(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Sweet).all()

# 🔒 UPDATE (ADMIN)
@router.put("/{sweet_id}")
def update_sweet(
    sweet_id: int,
    data: SweetUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(404, "Sweet not found")

    sweet.name = data.name
    sweet.category = data.category
    sweet.price = data.price
    sweet.quantity = data.quantity

    db.commit()
    db.refresh(sweet)
    return sweet

# 🔒 DELETE (ADMIN)
@router.delete("/{sweet_id}")
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(404, "Sweet not found")

    db.delete(sweet)
    db.commit()
    return {"message": "Sweet deleted"}

@router.post("/{sweet_id}/purchase")
def purchase_sweet(
    sweet_id: int,
    quantity: int = Query(1, gt=0),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()

    if sweet is None:
        raise HTTPException(status_code=404, detail="Sweet not found")

    if sweet.quantity < quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available"
        )

    sweet.quantity -= quantity
    db.commit()
    db.refresh(sweet)

    return {
        "message": "Purchase successful",
        "remaining_quantity": sweet.quantity
    }


# 🔒 RESTOCK (ADMIN)
@router.post("/{sweet_id}/restock")
def restock_sweet(
    sweet_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(404, "Sweet not found")

    sweet.quantity += quantity
    db.commit()
    return {"new_quantity": sweet.quantity}


from app.schemas.sweet import SweetCreate

# ➕ ADD SWEET (ADMIN ONLY)
@router.post("/", status_code=201)
def add_sweet(
    data: SweetCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    sweet = Sweet(
        name=data.name,
        category=data.category,
        price=data.price,
        quantity=data.quantity
    )

    db.add(sweet)
    db.commit()
    db.refresh(sweet)

    return sweet


@router.get("/search")
def search_sweets(
    name: str | None = Query(default=None),
    category: str | None = Query(default=None),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Sweet)

    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)

    return query.all()
