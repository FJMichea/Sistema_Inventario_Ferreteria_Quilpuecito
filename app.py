from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_super_segura' # Necesario para manejar sesiones

def get_db_connection():
    conn = sqlite3.connect('ferreteria.db')
    conn.row_factory = sqlite3.Row
    # Importante: Activar soporte para Foreign Keys en SQLite
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Esta función verifica si estás logueado antes de dejarte entrar a una ruta
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # Esta ruta es temporal, solo para crear tu primer usuario admin
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Encriptamos la contraseña antes de guardarla
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)',
                         (username, hashed_password))
            conn.commit()
            flash('Usuario creado exitosamente. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El usuario ya existe.', 'danger')
        finally:
            conn.close()
            
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        # Verificamos si el usuario existe y si la contraseña coincide con el hash
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Bienvenido al sistema.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() # Borra la sesión
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))


@app.route('/')
@login_required # <--- Protección activada
def index():
    return render_template('index.html')

@app.route('/productos')
@login_required
def productos():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/trabajadores')
@login_required
def trabajadores():
    conn = get_db_connection()
    trabajadores = conn.execute('SELECT * FROM trabajadores').fetchall()
    conn.close()
    return render_template('trabajadores.html', trabajadores=trabajadores)

@app.route('/asignar', methods=['GET', 'POST'])
@login_required
def asignar():
    conn = get_db_connection()
    
    if request.method == 'POST':
        producto_id = request.form['producto_id']
        trabajador_id = request.form['trabajador_id']
        cantidad = int(request.form['cantidad']) # Convertir a entero

        # 1. Verificar si hay suficiente stock
        producto_actual = conn.execute('SELECT cantidad FROM productos WHERE id = ?', (producto_id,)).fetchone()
        
        if producto_actual and producto_actual['cantidad'] >= cantidad:
            # 2. Registrar la asignación
            conn.execute('INSERT INTO asignaciones (producto_id, trabajador_id, cantidad) VALUES (?, ?, ?)',
                         (producto_id, trabajador_id, cantidad))
            
            # 3. MEJORA: Descontar del inventario
            conn.execute('UPDATE productos SET cantidad = cantidad - ? WHERE id = ?',
                         (cantidad, producto_id))
            
            conn.commit()
            flash('Asignación realizada y stock actualizado.', 'success')
            conn.close()
            return redirect('/')
        else:
            flash('Error: No hay suficiente stock para realizar esta asignación.', 'danger')

    # Cargar listas para los select
    productos = conn.execute('SELECT * FROM productos').fetchall()
    trabajadores = conn.execute('SELECT * FROM trabajadores').fetchall()
    conn.close()
    return render_template('asignar.html', productos=productos, trabajadores=trabajadores)

@app.route('/registrar_merma', methods=['GET', 'POST'])
@login_required
def registrar_merma():
    conn = get_db_connection()
    
    if request.method == 'POST':
        producto_id = request.form['producto_id']
        merma = int(request.form['merma'])

        # Actualizamos la merma y también descontamos del stock físico disponible
        conn.execute('UPDATE productos SET merma = merma + ?, cantidad = cantidad - ? WHERE id = ?',
                     (merma, merma, producto_id))
        conn.commit()
        conn.close()
        flash('Merma registrada correctamente.', 'warning')
        return redirect('/productos')

    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('registrar_merma.html', productos=productos)

@app.route('/agregar_producto', methods=('GET', 'POST'))
@login_required
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
        flash('Producto agregado exitosamente.', 'success')
        return redirect('/productos')
    return render_template('agregar_producto.html')

if __name__ == '__main__':
    app.run(debug=True)
