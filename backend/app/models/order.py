from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    sweet_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
