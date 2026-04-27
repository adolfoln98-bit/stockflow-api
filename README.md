# StockFlow API

API REST desarrollada con FastAPI para la gestión de productos e inventario. Permite realizar operaciones CRUD completas, aplicar filtros dinámicos, paginación y ordenación de resultados.

---

## Tecnologías utilizadas

* Python
* FastAPI
* SQLite
* SQL
* Uvicorn

---

## Funcionalidades

* CRUD completo de productos
* Filtros dinámicos:

  * Nombre
  * Categoría
  * Precio mínimo y máximo
  * Stock mínimo
* Paginación (`limit` y `offset`)
* Ordenación por diferentes campos (`sort_by`, `order`)
* Validación de datos con Pydantic
* Arquitectura modular (routes, services, schemas, db)
* Inicialización automática de base de datos
* Generación de datos de prueba (seed)

---

## Estructura del proyecto

```
app/
├── main.py
├── db.py
├── schemas.py
├── routes/
│   └── productos.py
├── services/
│   └── productos_service.py
└── data/
    └── productos.db
```

---

## Instalación y ejecución

1. Clonar el repositorio:

```
git clone https://github.com/TU_USUARIO/stockflow-api.git
cd stockflow-api
```

2. Crear entorno virtual:

```
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:

```
pip install -r requirements.txt
```

4. Ejecutar servidor:

```
uvicorn app.main:app --reload
```

---

## Documentación

Una vez iniciado el servidor, acceder a:

* Swagger UI:
  http://127.0.0.1:8000/docs

---

## Ejemplos de uso

### Obtener productos con filtros

```
GET /api/productos?categoria=tecnologia&precio_min=50&sort_by=precio&order=desc
```

### Crear producto

```
POST /api/productos
```

Body:

```json
{
  "nombre": "Producto ejemplo",
  "descripcion": "Descripción del producto",
  "precio": 99.99,
  "stock": 10,
  "categoria": "tecnologia"
}
```

---

## Objetivo del proyecto

Este proyecto forma parte de mi proceso de aprendizaje en backend con Python, centrado en el desarrollo de APIs REST escalables y bien estructuradas.

---

##  Autor

Adolfo López Navas
[LinkedIn](https://www.linkedin.com/in/adolfolópeznavas)
