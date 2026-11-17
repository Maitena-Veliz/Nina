import sqlite3

con = sqlite3.connect("Nina.db")
print(con.execute("SELECT * FROM Producto").fetchall())
print(con.execute("SELECT * FROM Notificaciones").fetchall())
con.close()