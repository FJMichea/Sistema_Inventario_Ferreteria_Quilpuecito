from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('ferreteria.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/trabajadores')
def trabajadores():
    conn = get_db_connection()
    trabajadores = conn.execute('SELECT * FROM trabajadores').fetchall()
    conn.close()
    return render_template('trabajadores.html', trabajadores=trabajadores)

@app.route('/asignar', methods=['GET', 'POST'])
def asignar():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    trabajadores = conn.execute('SELECT * FROM trabajadores').fetchall()

    if request.method == 'POST':
        producto_id = request.form['producto_id']
        trabajador_id = request.form['trabajador_id']
        cantidad = request.form['cantidad']

        conn.execute('INSERT INTO asignaciones (producto_id, trabajador_id, cantidad) VALUES (?, ?, ?)',
                     (producto_id, trabajador_id, cantidad))
        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template('asignar.html', productos=productos, trabajadores=trabajadores)

@app.route('/registrar_merma', methods=['GET', 'POST'])
def registrar_merma():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()

    if request.method == 'POST':
        producto_id = request.form['producto_id']
        merma = request.form['merma']

        conn.execute('UPDATE productos SET merma = merma + ? WHERE id = ?',
                     (merma, producto_id))
        conn.commit()
        conn.close()
        return redirect('/productos')

    conn.close()
    return render_template('registrar_merma.html', productos=productos)


@app.route('/agregar_producto', methods=('GET', 'POST'))
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        conn = get_db_connection()
        conn.execute('INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)',
                     (nombre, cantidad, precio))
        conn.commit()
        conn.close()
        return redirect('/productos')
    return render_template('agregar_producto.html')

if __name__ == '__main__':
    app.run(debug=True)
