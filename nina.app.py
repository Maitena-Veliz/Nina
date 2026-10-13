from flask import Flask, render_template

import sqlite3

app= Flask(__name__)

@app.route('/')
def index():
    conexion = sqlite3.connect('Nina.db')
    cursor = conexion.cursor()

    cursor.execute("""
        select * from clientes
    """)

    # fetchall obtiene los datos que vienen de un select
    tabla = cursor.fetchall()
    return render_template("index.html",tabla=tabla)

    conexion.commit() #Confirma los cambios
    conexion.close() #Cierra la conexion con la base de datos



if __name__ == '__main__':
    app.run(debug=True)