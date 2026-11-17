import tkinter as tk
import sqlite3
from tkinter import messagebox

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
        FROM Producto
        WHERE stock = 0
    """)
    con.commit()
    con.close()


def agregar_producto(nombre, color, talle, precio, stock=0):    # GUARDA PRODUCTO NUEVO. SI ENTRA SIN STOCK, VA A NOTIS
    con = sqlite3.connect(DB)

    fila = con.execute("SELECT MAX(id_producto) FROM Producto").fetchone()
    ultimo = fila[0]

    if ultimo is None:
        nuevo_id = 1
    else:
        nuevo_id = ultimo + 1

    con.execute(
        "INSERT INTO Producto (id_producto, nombre, color, talle, precio, stock) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (nuevo_id, nombre, color, talle, precio, stock),
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


####################################################################################################################################################################

ventana = tk.Tk()
ventana.title("NINA")
ventana.geometry("800x700")
ventana.configure(bg="#C7C8CA")

#texto
etiqueta = tk.Label(ventana, text="Producto", font=("Arial", 12), bg="#C7C8CA",  fg="#333333")
etiqueta.grid(row=0, column=0, padx=20, pady=10)
#entry
entrada_Producto = tk.Entry(ventana)
entrada_Producto.grid(row=0, column=1, padx=10, pady=10)

#texto
etiqueta = tk.Label(ventana, text="Color", font=("Arial", 12), bg="#C7C8CA", fg="#333333")
etiqueta.grid(row=1, column=0, padx=20, pady=10)

#entry
entrada_color = tk.Entry(ventana)
entrada_color.grid(row=1, column=1, padx=10, pady=10)

#texto
etiqueta = tk.Label(ventana, text="Talle", font=("Arial", 12), bg="#C7C8CA", fg="#333333")
etiqueta.grid(row=2, column=0,padx=20, pady=10 )
#entry
entrada_talle = tk.Entry(ventana)
entrada_talle.grid(row=2, column=1, padx=10, pady=10)

#texto
etiqueta = tk.Label(ventana, text="Precio", font=("Arial", 12), bg="#C7C8CA", fg="#333333")
etiqueta.grid(row=3, column=0, padx=20, pady=10)
#entry
entrada_precio = tk.Entry(ventana)
entrada_precio.grid(row=3, column=1, padx=10, pady=10)

#texto
etiqueta = tk.Label(ventana, text="Stock", font=("Arial", 12), bg="#C7C8CA", fg="#333333")
etiqueta.grid(row=4, column=0, padx=20, pady=10)
#entry
entrada_stock = tk.Entry(ventana)
entrada_stock.grid(row=4, column=1, padx=10, pady=10)

def guardar():
    producto = entrada_Producto.get()
    color = entrada_color.get()
    talle = entrada_talle.get()
    precio = float(entrada_precio.get())
    stock = int(entrada_stock.get())

    agregar_producto(producto, color, talle, precio, stock)

    if stock == 0:
        mostrar_notificacion(producto)
    #    messagebox.showwarning("Sin stock", "...")

def mostrar_notificacion(producto):
    ventana_noti = tk.Toplevel()
    ventana_noti.title("Sin stock")
    ventana_noti.geometry("350x180")
    ventana_noti.configure(bg="#C4DAFA")

    tk.Label(
        ventana_noti,
        text="Producto sin stock",
        font=("Arial", 16, "bold"),
        bg="#C4DAFA",
        fg="#0833A2"
    ).pack(pady=15)

    tk.Label(
        ventana_noti,
        text=f"El producto '{producto}' no tiene stock.",
        font=("Arial", 11),
        bg="#C4DAFA"
    ).pack(pady=10)

    tk.Button(
        ventana_noti,
        text="Aceptar",
        font=("Arial", 12, "bold"),
        bg="#0833A2",
        fg="white",
        width=15,
        command=ventana_noti.destroy
    ).pack(pady=15)

boton = tk.Button(ventana, text="Guardar",font=("Arial", 12, "bold"), bg="#0833A2", fg="white", command=guardar)
boton.grid(row=5, column=0, columnspan=2, sticky="ew")

ventana.mainloop()