from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, description="Nome do produto")
    description: Optional[str] = Field(None, description="Descrição opcional do produto")
    price: float = Field(..., gt=0.0, description="Preço do produto (deve ser maior que zero)")
    stock: int = Field(..., ge=0, description="Estoque do produto (deve ser maior ou igual a zero)")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
