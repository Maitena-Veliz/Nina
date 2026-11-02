import sqlite3

DB = "Nina.db" 


def revisar_producto(nombre):           # REVISAR SI HAY STOCK
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


def agregar_producto(nombre, color, talle, precio, stock=0):         # BUSCAR PRODUCTO
    """Guarda un producto nuevo (lo usa el botón 'guardar')."""
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO productos (nombre, color, talle, precio, stock) "
        "VALUES (?, ?, ?, ?, ?)",
        (nombre, color, talle, precio, stock),
    )
    con.commit()
    con.close()
    
#### Acá hacer lo del notificaciones ####

def generar_notificaciones():     # COPIA A NOTIFICACIONES LOS PRODUCTOS SIN STOCK
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

#### Si queremos poner que ya hay stock, y "agregamos" cuantos productos hay,
### tenemos la funcion de borrar las notificaciones de lo productos que ya volvieron a tener stock

#def limpiar_notificaciones_repuestas():    #BORRA LAS NOTIS DE LOS PRODUCTOS QUE YA TIENEN STOCK
    #con = sqlite3.connect(DB)
    #con.execute("""
        #DELETE FROM Notificaciones
        #WHERE id_producto IN (
            #SELECT id_producto FROM productos WHERE stock > 0
        #)
    #""")
    #con.commit()
    #con.close()


def obtener_notificaciones():     # DEVUELVE LA LISTA DE PRODUCTOS SIN STOCK
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    filas = con.execute("SELECT * FROM Notificaciones").fetchall()
    con.close()
    return filas
