i# backend.py
import sqlite3

DB = "Nina.db"   # poné el nombre real de tu base


def revisar_producto(nombre):
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


def agregar_producto(nombre, color, talle, precio, stock=0):
    """Guarda un producto nuevo (lo usa el botón 'guardar')."""
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO productos (nombre, color, talle, precio, stock) "
        "VALUES (?, ?, ?, ?, ?)",
        (nombre, color, talle, precio, stock),
    )
    con.commit()
    con.close()
