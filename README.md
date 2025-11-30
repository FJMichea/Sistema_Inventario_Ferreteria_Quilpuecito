# 🛠️ Sistema de Gestión de Inventario - Ferretería Quilpuecito v2.0

> **Trabajo de Aplicación Práctica (TAP) - Analista Programador y Análisis de Sistemas** > *Una solución robusta, escalable y eficiente para la administración de activos y stock.*

---

## 📖 Descripción del Proyecto

Bienvenido al repositorio oficial del **Sistema de Gestión de Inventario para Ferretería Quilpuecito**. Este proyecto nace como una respuesta tecnológica a la necesidad de digitalizar procesos manuales, minimizar mermas y garantizar la trazabilidad de herramientas y productos.

En su versión actual (**v2.0**), el sistema ha evolucionado de un registro básico a una **plataforma web integral** que incorpora seguridad, inteligencia de negocios (BI) y generación de documentación formal, demostrando la viabilidad de tecnologías ligeras como Flask y SQLite para entornos empresariales PYME.

---

## 🚀 Funcionalidades Principales

### 📊 Dashboard Gerencial (Business Intelligence)
- **Panel de Control Visual:** Gráficos interactivos (Chart.js) para monitorear el estado del inventario en tiempo real.
- **KPIs Automáticos:** Visualización instantánea del valor total del inventario, alertas de stock crítico (< 5 unidades) y conteo de mermas.

### 🛡️ Seguridad y Control de Acceso
- **Autenticación Robusta:** Sistema de Login y Registro con encriptación de contraseñas (`Werkzeug Security`).
- **Protección de Rutas:** Decoradores de sesión para restringir el acceso a usuarios no autorizados.

### 📦 Gestión de Inventario (CRUD Completo)
- **Administración Total:** Crear, editar y eliminar productos y trabajadores.
- **Búsqueda Inteligente:** Tablas dinámicas con filtros en tiempo real y paginación (**DataTables**), optimizadas para grandes volúmenes de datos.

### 📋 Asignaciones y Trazabilidad
- **Ciclo de Préstamo:** Asignación de herramientas a trabajadores con descuento automático de stock.
- **Devoluciones:** Proceso de retorno de activos que restaura el inventario disponible.
- **Respaldo Documental:** Generación automática de **Comprobantes en PDF** listos para firmar (`xhtml2pdf`), garantizando responsabilidad legal.

### ⚠️ Control de Pérdidas
- Módulo dedicado para el registro y auditoría de Mermas.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3, Flask (Microframework).
* **Base de Datos:** SQLite 3 (Relacional).
* **Frontend:** HTML5, CSS3, Bootstrap 5 (Diseño Responsivo).
* **Librerías Clave:**
    * `Werkzeug`: Seguridad y Hashing.
    * `xhtml2pdf`: Motor de reportes PDF.
    * `Chart.js`: Visualización de datos.
    * `DataTables` + `jQuery`: Interfaz de tablas avanzadas.

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en un entorno local o en GitHub Codespaces.

### 1. Prerrequisitos del Sistema (Importante para PDF)
Para que la generación de PDFs funcione, es necesario instalar las librerías gráficas del sistema operativo (Cairo).

**En Linux / GitHub Codespaces:**
```bash
sudo apt-get update
sudo apt-get install -y libcairo2-dev pkg-config python3-dev

2. Clonar el Repositorio

git clone [https://github.com/FJMichea/Sistema_Inventario_Ferreteria_Quilpuecito.git](https://github.com/FJMichea/Sistema_Inventario_Ferreteria_Quilpuecito.git)
cd Sistema_Inventario_Ferreteria_Quilpuecito

3. Entorno Virtual y Dependencias Python

# Crear entorno virtual (Opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar librerías de Python
pip install Flask werkzeug xhtml2pdf

4. Inicialización de Base de Datos
El proyecto incluye scripts para configurar la base de datos automáticamente con datos de prueba.

# 1. Crear estructura de tablas (Usuarios, Productos, Trabajadores, Asignaciones)
python -c "import sqlite3; conn = sqlite3.connect('ferreteria.db'); conn.executescript(open('schema.sql').read()); conn.close()"

# 2. Cargar datos ficticios (Seed Data)
python cargar_datos.py

5. Ejecutar la Aplicación

python app.py

El sistema estará disponible en: http://127.0.0.1:5000

👤 Autor
Francisco J. Michea Analista Programador / Análisis de Sistemas AIEP

Este proyecto representa un compromiso con la mejora continua y la aplicación práctica de conocimientos en desarrollo de software.


## Capturas de Pantalla


* **Página de Inicio:**
    ![Página de Inicio]<img width="468" alt="image" src="https://github.com/user-attachments/assets/c1299b08-59be-4c1e-89f0-b4eeefdb081e" />
) 
* **Listado de Productos:**
    ![Listado de Productos](<img width="468" alt="image" src="https://github.com/user-attachments/assets/efd26cea-a91d-46b5-bd9b-bab43c3c9ebd" />
) 
* **Formulario para Agregar Productos:**
    ![Formulario Agregar Productos](<img width="468" alt="image" src="https://github.com/user-attachments/assets/fc7b07a1-e519-4f46-94c7-378c1956ce52" />
) 
* **Listado de Trabajadores:**
    ![Listado de Trabajadores](<img width="468" alt="image" src="https://github.com/user-attachments/assets/2e242f5c-9261-4406-8cd9-27f7eb7e4fb2" />
) 
* **Formulario para Asignaciones:**
    ![Formulario Asignaciones](<img width="468" alt="image" src="https://github.com/user-attachments/assets/bde79498-9ced-4f55-8154-459e0c202ed5" />
) 
* **Formulario para Registrar Merma:**
    ![Formulario Registrar Merma](<img width="468" alt="image" src="https://github.com/user-attachments/assets/b9ea8a71-47e1-41a5-8b42-3d89c49aa868" />
) 
* **Vista de la Base de Datos en DB Browser:**
    ![Vista DB Browser](<img width="468" alt="image" src="https://github.com/user-attachments/assets/a4d38126-521f-48ca-9270-214e193fc169" />
) 
* **Tablero Kanban (Ejemplo):**
    ![Tablero Kanban](<img width="396" alt="image" src="https://github.com/user-attachments/assets/23c93b4e-e4c0-4a14-804c-05255926a520" />
) 
* **Comandos en Terminal:**
    ![Terminal Commands](<img width="468" alt="image" src="https://github.com/user-attachments/assets/019e4ff7-648a-4030-80ee-d33bdfc0ee77" />
) 


## Conclusiones y Reflexiones

El desarrollo de este sistema permitió la aplicación práctica de conocimientos en desarrollo backend, bases de datos y planificación ágil. Se comprobó que tecnologías ligeras como Flask y SQLite son viables para las necesidades de pequeñas empresas. Este proyecto no solo representa una solución técnica funcional, sino también un ejemplo del compromiso con la mejora continua y la aplicación práctica del conocimiento adquirido durante la formación profesional.

## Mejoras Futuras

Se proponen las siguientes mejoras para futuras iteraciones del sistema:
* Integrar autenticación de usuarios para control de acceso.
* Generación de reportes en formato PDF.
* Mejoras visuales en la interfaz de usuario con CSS o Bootstrap.
