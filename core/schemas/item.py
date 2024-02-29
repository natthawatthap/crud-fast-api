from pydantic import BaseModel, Field, validator

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than zero')
        return v
