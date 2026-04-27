from pydantic import BaseModel, Field

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=80)
    descripcion: str | None = Field(None, max_length=255)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: str | None = Field(None, max_length=50)

class Producto(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id: int
    creado_en: str | None = None

class ProductosResponse(BaseModel):
    data: list[ProductoOut]
    total: int
    limit: int
    offset: int