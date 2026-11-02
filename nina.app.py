import sqlite3

DB = "Nina.db"

def buscar_producto(texto):    # BUSCA POR NOMBRE, COLOR, TALLE O PRECIO
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    filas = con.execute(
        """
        SELECT * FROM productos
        WHERE nombre LIKE ?
           OR color  LIKE ?
           OR talle  LIKE ?
           OR precio LIKE ?
        """,
        (f"%{texto}%",) * 4,
    ).fetchall()
    con.close()
    return filas

def revisar_producto(nombre):    # REVISA SI HAY STOCK DE UN PRODUCTO
    """Busca por nombre y dice si hay stock o no."""
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    fila = con.execute(
        "SELECT * FROM productos WHERE nombre = ?", (nombre,)
    ).fetchone()
    con.close()

    if fila is None:
        return "No existe ese producto"
    elif fila["stock"] == 0:
        return f"{fila['nombre']}: sin stock"
    else:
        return f"{fila['nombre']}: disponible, ${fila['precio']}"


def generar_notificaciones():    # COPIA A NOTIFICACIONES LOS PRODUCTOS SIN STOCK
    con = sqlite3.connect(DB)
    con.execute("""
        INSERT OR IGNORE INTO Notificaciones
            (id_producto, stock, nombre, precio, color, talle)
        SELECT id_producto, stock, nombre, precio, color, talle
        FROM productos
        WHERE stock = 0
    """)
    con.commit()
    con.close()


def agregar_producto(nombre, color, talle, precio, stock=0):    # GUARDA PRODUCTO NUEVO. SI ENTRA SIN STOCK, VA A NOTIS
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO productos (nombre, color, talle, precio, stock) "
        "VALUES (?, ?, ?, ?, ?)",
        (nombre, color, talle, precio, stock),
    )
    con.commit()
    con.close()

    if stock == 0:
        generar_notificaciones()


def obtener_notificaciones():    # DEVUELVE LA LISTA DE PRODUCTOS SIN STOCK
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    filas = con.execute("SELECT * FROM Notificaciones").fetchall()
    con.close()
    return filas


def agregar_stock_notificacion(id_producto, cantidad):    # SUMA STOCK AL PRODUCTO Y LO SACA DE NOTIS
    if cantidad <= 0:
        return "La cantidad tiene que ser mayor a 0"

    con = sqlite3.connect(DB)
    cur = con.execute(
        "UPDATE productos SET stock = stock + ? WHERE id_producto = ?",
        (cantidad, id_producto),
    )
    if cur.rowcount == 0:
        con.close()
        return "No existe ese producto"

    con.execute(
        "DELETE FROM Notificaciones WHERE id_producto = ?", (id_producto,)
    )
    con.commit()
    con.close()
    return "Stock actualizado"
