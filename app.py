from io import BytesIO
from xhtml2pdf import pisa
from flask import make_response
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

# --- DECORADOR DE SEGURIDAD ---
# Esta función verifica si estás logueado antes de dejarte entrar a una ruta
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- RUTAS DE AUTENTICACIÓN ---

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

# --- RUTAS DEL SISTEMA (Ahora protegidas) ---

@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    
    # --- 1. CÁLCULO DE INDICADORES (KPIs) ---
    # Total de productos únicos registrados
    total_items = conn.execute('SELECT COUNT(*) FROM productos').fetchone()[0]
    
    # Productos con stock crítico (menos de 5 unidades)
    stock_critico = conn.execute('SELECT COUNT(*) FROM productos WHERE cantidad < 5').fetchone()[0]
    
    # Valor total del inventario (Dinero invertido en bodega)
    valor_inventario = conn.execute('SELECT SUM(cantidad * precio) FROM productos').fetchone()[0]
    # Si no hay productos, valor_inventario podría ser None, lo cambiamos a 0
    if valor_inventario is None: valor_inventario = 0

    # Total de Mermas registradas
    total_mermas = conn.execute('SELECT SUM(merma) FROM productos').fetchone()[0] or 0
    
    # --- 2. DATOS PARA GRÁFICOS ---
    
    # Gráfico 1: Top 5 Productos con mayor Stock
    top_stock = conn.execute('SELECT nombre, cantidad FROM productos ORDER BY cantidad DESC LIMIT 5').fetchall()
    # Separamos en dos listas para pasarlas fácil a Chart.js
    nombres_stock = [row['nombre'] for row in top_stock]
    cantidades_stock = [row['cantidad'] for row in top_stock]
    
    # Gráfico 2: Top 5 Productos con más Mermas (Pérdidas)
    top_mermas = conn.execute('SELECT nombre, merma FROM productos WHERE merma > 0 ORDER BY merma DESC LIMIT 5').fetchall()
    nombres_mermas = [row['nombre'] for row in top_mermas]
    cantidades_mermas = [row['merma'] for row in top_mermas]
    
    conn.close()
    
    return render_template('index.html',
                           total_items=total_items,
                           stock_critico=stock_critico,
                           valor_inventario=valor_inventario,
                           total_mermas=total_mermas,
                           nombres_stock=nombres_stock,
                           cantidades_stock=cantidades_stock,
                           nombres_mermas=nombres_mermas,
                           cantidades_mermas=cantidades_mermas)

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

# --- RUTAS PARA GESTIONAR TRABAJADORES (EDITAR / ELIMINAR) ---

@app.route('/eliminar_trabajador/<int:id>')
@login_required
def eliminar_trabajador(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM trabajadores WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Trabajador eliminado correctamente.', 'warning')
    return redirect(url_for('trabajadores'))

@app.route('/editar_trabajador/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_trabajador(id):
    conn = get_db_connection()
    
    # Si enviamos el formulario (POST), actualizamos los datos
    if request.method == 'POST':
        nombre = request.form['nombre']
        cargo = request.form['cargo']
        
        conn.execute('UPDATE trabajadores SET nombre = ?, cargo = ? WHERE id = ?',
                     (nombre, cargo, id))
        conn.commit()
        conn.close()
        flash('Datos del trabajador actualizados.', 'success')
        return redirect(url_for('trabajadores'))

    # Si entramos a la página (GET), cargamos los datos actuales para mostrarlos
    trabajador = conn.execute('SELECT * FROM trabajadores WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if trabajador is None:
        flash('Trabajador no encontrado.', 'danger')
        return redirect(url_for('trabajadores'))
        
    return render_template('editar_trabajador.html', trabajador=trabajador)
    
    # --- GESTIÓN DE PRODUCTOS (EDITAR / ELIMINAR) ---

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    conn = get_db_connection()
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        # Nota: No permitimos editar cantidad directamente para no romper la lógica de mermas/asignaciones
        # La cantidad se ajusta por asignación o merma.
        
        conn.execute('UPDATE productos SET nombre = ?, precio = ? WHERE id = ?',
                     (nombre, precio, id))
        conn.commit()
        conn.close()
        flash('Producto actualizado.', 'success')
        return redirect(url_for('productos'))

    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar_producto/<int:id>')
@login_required
def eliminar_producto(id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM productos WHERE id = ?', (id,))
        conn.commit()
        flash('Producto eliminado.', 'warning')
    except sqlite3.IntegrityError:
        flash('No se puede eliminar: El producto tiene asignaciones o mermas asociadas.', 'danger')
    finally:
        conn.close()
    return redirect(url_for('productos'))

# --- GESTIÓN DE ASIGNACIONES (VER Y DEVOLVER) ---

@app.route('/mis_asignaciones')
@login_required
def mis_asignaciones():
    conn = get_db_connection()
    # Consulta compleja (JOIN) para traer nombres en lugar de solo IDs
    query = '''
        SELECT a.id, p.nombre as producto, t.nombre as trabajador, a.cantidad, a.fecha
        FROM asignaciones a
        JOIN productos p ON a.producto_id = p.id
        JOIN trabajadores t ON a.trabajador_id = t.id
        ORDER BY a.fecha DESC
    '''
    asignaciones = conn.execute(query).fetchall()
    conn.close()
    return render_template('mis_asignaciones.html', asignaciones=asignaciones)

@app.route('/devolver_asignacion/<int:id>')
@login_required
def devolver_asignacion(id):
    conn = get_db_connection()
    
    # 1. Obtener datos de la asignación antes de borrarla
    asignacion = conn.execute('SELECT producto_id, cantidad FROM asignaciones WHERE id = ?', (id,)).fetchone()
    
    if asignacion:
        # 2. Devolver el stock al inventario
        conn.execute('UPDATE productos SET cantidad = cantidad + ? WHERE id = ?',
                     (asignacion['cantidad'], asignacion['producto_id']))
        
        # 3. Borrar la asignación (o podríamos moverla a una tabla 'historial_devoluciones' si quisieras ser más pro)
        conn.execute('DELETE FROM asignaciones WHERE id = ?', (id,))
        
        conn.commit()
        flash('Herramienta devuelta. Stock restaurado.', 'success')
    else:
        flash('Error al intentar devolver.', 'danger')
        
    conn.close()
    return redirect(url_for('mis_asignaciones'))

# --- GENERACIÓN DE PDF ---

@app.route('/generar_pdf/<int:id>')
@login_required
def generar_pdf(id):
    conn = get_db_connection()
    
    # 1. Obtenemos todos los datos de esa asignación específica
    query = '''
        SELECT a.id, a.fecha, a.cantidad, 
               p.nombre as producto, p.precio, 
               t.nombre as trabajador, t.cargo
        FROM asignaciones a
        JOIN productos p ON a.producto_id = p.id
        JOIN trabajadores t ON a.trabajador_id = t.id
        WHERE a.id = ?
    '''
    asignacion = conn.execute(query, (id,)).fetchone()
    conn.close()
    
    if not asignacion:
        flash('Asignación no encontrada.', 'danger')
        return redirect(url_for('mis_asignaciones'))

    # 2. Renderizamos el HTML del PDF (usaremos una plantilla nueva)
    html = render_template('pdf_comprobante.html', a=asignacion)
    
    # 3. Convertimos el HTML a PDF usando xhtml2pdf
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=pdf)
    
    # 4. Si no hubo errores, descargamos el archivo
    if not pisa_status.err:
        pdf.seek(0)
        response = make_response(pdf.read())
        # Esto hace que el navegador descargue el archivo con nombre "Comprobante_ID.pdf"
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=Comprobante_{id}.pdf'
        return response
    
    flash('Error al generar el PDF.', 'danger')
    return redirect(url_for('mis_asignaciones'))


if __name__ == '__main__':
    app.run(debug=True)