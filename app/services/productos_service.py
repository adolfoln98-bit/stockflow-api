from db import conn
from schemas import Producto




def fila_a_producto(fila):
    return dict(fila)

def db_a_json (lista_db):
    resultado = []

    for producto in lista_db:
        resultado.append(fila_a_producto(producto))

    return resultado


def construir_metadatos(data: list, total: int, limit: int, offset: int):
    return {
        "data": db_a_json(data),
        "total": total,
        "limit": limit,
        "offset": offset
    }


def listar_productos(
        nombre: str = None,
        categoria: str = None,
        precio_min: float = None,
        precio_max: float = None,
        stock_min: int = None,
        limit: int = 10,
        offset: int = 0,
        sort_by: str= "id",
        order: str="asc"
    ):
    query = "SELECT * FROM productos"
    count_query = "SELECT COUNT(*) FROM productos"

    condiciones = []
    valores = []

    campos_validos = ["id", "nombre", "precio", "stock", "categoria", "creado_en"]
    orden_valido = ["asc", "desc"]

    order = order.lower()

    if sort_by not in campos_validos:
        raise ValueError("Campo de ordenación no válido")
    
    if order not in orden_valido:
        raise ValueError("Campo de orden no valido")
    
    if precio_min is not None and precio_max is not None and precio_min > precio_max:
        raise ValueError("El precio minimo no puede ser mayor al precio maximo")
    
    
    if nombre:
        condiciones.append("nombre LIKE ?")
        valores.append(f"%{nombre}%")

    if categoria:
        condiciones.append("categoria LIKE ?")
        valores.append(f"%{categoria}%")

    if precio_min is not None:
        condiciones.append("precio >= ?")
        valores.append(precio_min)

    if precio_max is not None:
        condiciones.append("precio <= ?")
        valores.append(precio_max)

    if stock_min is not None:
        condiciones.append("stock >= ?")
        valores.append(stock_min)

    if condiciones:
        query += " WHERE "+" AND ".join(condiciones)
        count_query += " WHERE "+" AND ".join(condiciones)
    
    query += f" ORDER BY {sort_by} {order} LIMIT ? OFFSET ?"

    valores_finales = valores + [limit, offset]

    with conn() as conexion:
        cursor = conexion.cursor()

        cursor.execute(count_query, valores)
        total_respuestas = cursor.fetchone()[0]

        cursor.execute(query, valores_finales)
        respuesta_db = cursor.fetchall()

    
    return construir_metadatos(respuesta_db, total_respuestas, limit, offset)

def buscar_producto_id(id: int):
    with conn() as conexion:
        cursor = conexion.cursor()

        cursor.execute("""
        Select * from productos where id = ?
        """, (id,))

        producto = cursor.fetchone()

    if producto is None:
        return None
    
    return fila_a_producto(producto)

def crear_nuevo_producto_db(producto: Producto):
    with conn() as conexion:
        cursor = conexion.cursor()

        cursor.execute("""
        Insert into productos (nombre, descripcion, precio, stock, categoria)
        values(?, ?, ?, ?, ?)
        """, (
            producto.nombre,
            producto.descripcion,
            producto.precio,
            producto.stock,
            producto.categoria
            ))

        conexion.commit()

        ultimo_id = cursor.lastrowid
        producto_creado = cursor.rowcount

    if producto_creado== 0:
        return None
    
    return buscar_producto_id(ultimo_id)

def actualizar_producto_db(id: int, producto: Producto):
    with conn() as conexion:
        cursor = conexion.cursor()


        cursor.execute("""
        Update productos
        set nombre = ?, descripcion= ?, precio= ?, stock= ?, categoria= ?
        where id = ?
        """, (producto.nombre,
              producto.descripcion,
              producto.precio,
              producto.stock,
              producto.categoria,
              id
              ))


        conexion.commit()


        if cursor.rowcount == 0:
            return None
        

        cursor.execute("""
            Select * from productos where id = ?
            """, (id,))
        
        
       
    return buscar_producto_id(id)
    
def borrar_producto_db(id: int):
    with conn() as conexion:
        cursor = conexion.cursor()


        cursor.execute("""
            DELETE FROM productos WHERE id = ? 
            """, (id,))
        

        conexion.commit()
        filas_borradas = cursor.rowcount

    return filas_borradas > 0