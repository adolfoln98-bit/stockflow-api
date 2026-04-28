from fastapi import FastAPI
from app.routes.productos import router as productos_router
from app.db import init_db, seed_data



app = FastAPI(
    title="StockFlow API",
    description="API REST para gestión de productos e inventario",
    version="1.0.0"
)

#inicializar base de datos
init_db()
seed_data()

app.include_router(productos_router, prefix="/api/productos", tags=["Productos"])
