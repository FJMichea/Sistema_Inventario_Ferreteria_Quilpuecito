import sqlite3

def cargar_datos():
    conn = sqlite3.connect('ferreteria.db')
    cursor = conn.cursor()

    # 1. Lista de Trabajadores solicitados
    trabajadores = [
        ('Juan Pérez', 'Administrador'),
        ('María González', 'Ventas'),
        ('Carlos Sánchez', 'Inventario'),
        ('Ana López', 'Cajas'),
        ('Pedro Ramírez', 'Despacho'),
        ('Luisa Fernández', 'Ventas'),
        ('Diego Castillo', 'Recepción de mercadería'),
        ('Claudia Morales', 'Atención al cliente')
    ]

    print("Cargando trabajadores...")
    cursor.executemany('INSERT INTO trabajadores (nombre, cargo) VALUES (?, ?)', trabajadores)

    # 2. Algunos Productos de prueba para que no esté vacío
    productos = [
        ('Martillo Carpintero', 50, 4500),
        ('Juego Destornilladores', 30, 8990),
        ('Taladro Percutor 500W', 15, 25990),
        ('Lija de Madera #100', 200, 500),
        ('Pintura Blanca 1GL', 20, 14990)
    ]

    print("Cargando productos...")
    cursor.executemany('INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)', productos)

    conn.commit()
    conn.close()
    print("¡Datos cargados exitosamente!")

if __name__ == '__main__':
    cargar_datos()