import sqlite3

DB_PATH = "data/productos.db"

def conn():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion

def init_db():
    with conn() as conexion:
        cursor = conexion.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            categoria TEXT,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conexion.commit()

def seed_data():
    with conn() as conexion:
        cursor = conexion.cursor()

        # Evitar duplicados (si ya hay datos, no inserta nada)
        cursor.execute("SELECT COUNT(*) FROM productos")
        total = cursor.fetchone()[0]

        if total > 0:
            return

        productos = [
            ("Teclado mecánico", "Teclado RGB con switches azules", 79.99, 15, "tecnologia"),
            ("Ratón inalámbrico", "Ratón ergonómico con batería recargable", 29.99, 30, "tecnologia"),
            ("Monitor 24 pulgadas", "Monitor Full HD IPS", 149.99, 10, "tecnologia"),
            ("Silla oficina", "Silla ergonómica con soporte lumbar", 199.99, 5, "muebles"),
            ("Escritorio madera", "Escritorio minimalista", 249.99, 3, "muebles"),
            ("Auriculares Bluetooth", "Cancelación de ruido", 89.99, 20, "tecnologia"),
            ("Camiseta básica", "Algodón 100%", 12.99, 50, "ropa"),
            ("Zapatillas deportivas", "Running ligero", 59.99, 25, "ropa"),
            ("Mochila", "Mochila resistente al agua", 39.99, 18, "accesorios"),
            ("Lámpara LED", "Luz regulable", 19.99, 40, "hogar")
        ]

        cursor.executemany("""
            INSERT INTO productos (nombre, descripcion, precio, stock, categoria)
            VALUES (?, ?, ?, ?, ?)
        """, productos)

        conexion.commit()