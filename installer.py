import sqlite3

conexion = sqlite3.connect('Nina.db')
cursor = conexion.cursor()


cursor.execute("PRAGMA foreign_keys = ON;")

# Ejecuta la consulta a la base de datos

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS Producto(
    id_producto INTEGER(50) not null PRIMARY KEY,
    stock INTEGER(50) not null,
    nombre VARCHAR(250) not null,
    precio INTEGER(50) not null,
    color VARCHAR(250) not null,
    talle VARCHAR(250) not null
    );
""")

#cursor.execute("""
#    INSERT INTO Producto (id_producto, stock, nombre, precio, color, talle) 
#    VALUES (01 , 20, 'Jean recto', 30000, 'Negro', '38');
#""")

cursor.execute("""
    INSERT INTO Producto (id_producto, stock, nombre, precio, color, talle) 
    VALUES (02 , 30, 'Jean baggy', 40000, 'Gris', '42');
""")

conexion.commit() #Confirma los cambios
conexion.close() #Cierra la conexion con la base de datos