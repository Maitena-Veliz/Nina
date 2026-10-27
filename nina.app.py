import tkinter

import sqlite3


conexion = sqlite3.connect('Nina.db')
cursor = conexion.cursor()

cursor.execute("""
    select * from clientes
""")

DB = "datos.db"

# fetchall obtiene los datos que vienen de un select
tabla = cursor.fetchall()
return render_template("index.html",tabla=tabla)

conexion.commit() #Confirma los cambios
conexion.close() #Cierra la conexion con la base de datos

def revisar_producto(nombre):              #BUSCAR POR STOCK/SI NO HAY STOCK
    con = sqlite3.connect("datos.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
    fila = cur.fetchone()
    con.close()

    if fila is None:
        return "No existe ese producto"
    elif fila["stock"] == 0:
        return f"{fila['nombre']}: sin stock"
    else:
        return f"{fila['nombre']}: disponible, ${fila['precio']}"

def buscar_producto(texto):
    """Busca en nombre, color, talle y precio. Devuelve una lista de filas."""
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
