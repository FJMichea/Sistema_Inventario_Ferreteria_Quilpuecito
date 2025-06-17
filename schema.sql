DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS trabajadores;
DROP TABLE IF EXISTS asignaciones;

CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    merma INTEGER DEFAULT 0
);

CREATE TABLE trabajadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cargo TEXT NOT NULL
);

CREATE TABLE asignaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER,
    trabajador_id INTEGER,
    fecha DATE DEFAULT CURRENT_DATE,
    cantidad INTEGER,
    FOREIGN KEY(producto_id) REFERENCES productos(id),
    FOREIGN KEY(trabajador_id) REFERENCES trabajadores(id)
);
