from pydantic import BaseModel

class SweetBase(BaseModel):
    name: str
    category: str
    price: int
    quantity: int

class SweetCreate(SweetBase):
    pass

class SweetUpdate(SweetBase):
    pass

class SweetResponse(SweetBase):
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel

class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int
