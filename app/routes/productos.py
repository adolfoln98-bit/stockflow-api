from fastapi import APIRouter, HTTPException, Query
from typing import Literal

from app.services.productos_service import (
    listar_productos,
    buscar_producto_id,
    crear_nuevo_producto_db,
    actualizar_producto_db,
    borrar_producto_db
    )

from app.schemas import Producto, ProductoOut, ProductosResponse



router = APIRouter()

@router.get("", response_model=ProductosResponse)
def buscar_producto(
                nombre: str | None = None,
                categoria: str | None = None,
                precio_min: float | None = Query(None, ge=0),
                precio_max: float | None = Query(None, ge=0),
                stock_min: int | None = Query(None, ge=0),
                limit: int = Query(10, ge=1),
                offset: int = Query(0, ge=0),
                sort_by: Literal["id", "nombre", "precio", "stock", "categoria", "creado_en"] = "id",
                order: Literal["asc", "desc"] = "asc"
    ):

    try:
        return listar_productos(
            nombre,
            categoria,
            precio_min,
            precio_max,
            stock_min,
            limit,
            offset,
            sort_by,
            order
        )
    
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{id}", response_model=ProductoOut)
def buscar_producto_id(id: int):
    producto = buscar_producto_id(id)

    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return producto


@router.post("", status_code=201, response_model=ProductoOut)
def crear_producto(producto: Producto):
    nuevo_producto = crear_nuevo_producto_db(producto)

    if nuevo_producto is None:
        raise HTTPException(status_code=400, detail="No se pudo añadir el producto")
    
    return nuevo_producto
        
       
@router.put("/{id}", response_model=ProductoOut)
def actualizar_producto(id: int, producto: Producto):  
    producto_actualizado = actualizar_producto_db(id, producto)  

    if producto_actualizado is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return producto_actualizado

@router.delete("/{id}")
def borrar_producto(id: int):
    producto_borrado = borrar_producto_db(id)

    if producto_borrado:
        return {"mensaje": "Producto borrado"}
    
    raise HTTPException(status_code=404, detail="Producto no encontrado")
    
