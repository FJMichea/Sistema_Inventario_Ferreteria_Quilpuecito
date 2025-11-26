# Sistema de Gestión de Inventario - Ferretería Quilpuecito

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un sistema de gestión web básico, diseñado para apoyar la organización interna de pequeñas empresas del rubro ferretero. Fue creado como Trabajo de Aplicación Práctica (TAP) para la carrera de Analista Programador y Análisis de Sistemas en AIEP.

La solución aborda problemáticas comunes en ferreterías que operan con procesos manuales o dispersos para el control de stock, asignaciones y pérdidas de productos. 
Generando errores, mermas y falta de trazabilidad. El sistema proporciona una herramienta eficiente y económica para digitalizar y organizar estos procesos.

## Funcionalidades Principales

El sistema implementado ofrece las siguientes características clave:

* **Gestión de Productos:** Permite registrar nuevos productos, visualizar un listado dinámico de los productos almacenados con su nombre, cantidad, precio y merma, y controlar el inventario en tiempo real.
* **Gestión de Trabajadores:** Despliega un listado de todos los trabajadores registrados, incluyendo nombre y cargo, fundamental para la asignación de productos.
* **Asignación de Productos:** Permite asignar productos específicos a trabajadores seleccionándolos desde listas desplegables, registrando la cantidad asignada.
* **Control de Merma:** Facilita el registro de pérdida o deterioro de productos, actualizando automáticamente la cantidad de merma asociada a cada producto en el sistema.
* **Informes Básicos:** Posibilidad de generar informes (ej. productos asignados por trabajador) mediante consultas directas a la base de datos, útil para supervisión interna y planificación de stock.

## Tecnologías Utilizadas

* **Lenguaje de Programación:** Python 
* **Framework Web:** Flask 
* **Base de Datos:** SQLite 
* **Interfaz de Usuario:** HTML 
* **Herramientas de Desarrollo:** Visual Studio Code , DB Browser for SQLite , Trello (simulado para gestión ágil) 

## Metodología de Desarrollo

Para la planificación y gestión de las actividades del proyecto, se utilizó la metodología ágil **Kanban**. Esto permitió dividir el trabajo en etapas claras y manejables, simulando un flujo de trabajo mediante columnas visuales (`Por hacer`, `En desarrollo`, `Terminado`) para organizar las tareas y cumplir con los tiempos establecidos.

## Estructura de la Base de Datos

El sistema utiliza una base de datos SQLite con las siguientes tablas principales:

* `productos`: Para almacenar la información de cada producto (ID, nombre, cantidad, precio, merma).
* `trabajadores`: Para registrar a los empleados (ID, nombre, cargo).
* `asignaciones`: Para registrar qué producto fue asignado a qué trabajador, incluyendo la cantidad y la fecha.

## Cómo Ejecutar el Proyecto

Para poner en marcha este sistema localmente, sigue los siguientes pasos:

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/FJMichea/Sistema_Inventario_Ferreteria_Quilpuecito.git](https://github.com/FJMichea/Sistema_Inventario_Ferreteria_Quilpuecito.git)
    cd Sistema_Inventario_Ferreteria_Quilpuecito
    ```
2.  **Configurar Entorno Virtual (Recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En macOS/Linux
    # venv\Scripts\activate.bat  # En Windows
    ```
3.  **Instalar Dependencias:**
    ```bash
    pip install Flask
    ```
    (Asegúrate de instalar cualquier otra dependencia si tu proyecto usa más que Flask).
4.  **Inicializar la Base de Datos:**
    El proyecto incluye un archivo `schema.sql`. Ejecútalo para crear la estructura de la base de datos:
    ```python
    # Puedes crear un pequeño script en Python (ej. init_db.py) para esto:
    # import sqlite3
    # conn = sqlite3.connect('ferreteria.db')
    # with open('schema.sql') as f:
    #     conn.executescript(f.read())
    # conn.close()
    ```
    O puedes usar `DB Browser for SQLite` para abrir `ferreteria.db` y cargar `schema.sql`.
5.  **Ejecutar la Aplicación Flask:**
    ```bash
    export FLASK_APP=app.py # En macOS/Linux
    # set FLASK_APP=app.py # En Windows
    flask run
    ```
    La aplicación se ejecutará en `http://127.0.0.1:5000`.


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

---
