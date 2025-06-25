# DynamicDBDiagrams - Generador de Diagramas de Base de Datos

Un proyecto de **Anthony Jafeth Arias Robleto**, **Luis Andrés Méndez Campos** y **Roosevelt Alejandro Pérez González**.

## 📝 Descripción

**DynamicDBDiagrams** es una herramienta web diseñada para simplificar y automatizar la visualización de estructuras de bases de datos. El sistema extrae los metadatos (tablas, columnas, claves primarias, relaciones, etc.) directamente del esquema de información de una base de datos relacional y genera automáticamente un diagrama UML. 

El objetivo principal es ofrecer a los desarrolladores y administradores de bases de datos una forma rápida y eficiente de obtener una representación visual clara y actualizada de la arquitectura de sus sistemas, eliminando la necesidad de dibujar diagramas manualmente y facilitando la documentación y el análisis. 

## ✨ Características Principales

* **Generación automática de diagramas:** Convierte la estructura de tu base de datos en un diagrama UML legible con un solo clic.
* **Compatibilidad multi-motor:** Soporta las bases de datos más populares:
    * PostgreSQL 
    * MySQL 
    * MS SQL Server 
* **Interfaz de usuario intuitiva:** Un panel lateral permite configurar fácilmente los parámetros de conexión a la base de datos. 
* **Visualización instantánea:** Muestra el diagrama generado directamente en la interfaz.
* **Historial de diagramas:** Guarda y muestra una lista de los diagramas generados anteriormente para una referencia rápida. 
* **Descarga de diagramas:** Permite descargar los diagramas generados en formato de imagen PNG. 

## 🚀 Tecnologías Utilizadas

El proyecto sigue una arquitectura cliente-servidor:

### **Frontend**

* **Framework:** React.js 
* **Estilos:** Bootstrap para componentes y CSS personalizado para el diseño. 
* **Empaquetador:** Rsbuild

### **Backend**

* **Framework:** FastAPI (Python) 
* **Conectores de Base de Datos:**
    * `psycopg2` para PostgreSQL 
    * `mysql-connector-python` para MySQL 
    * `pyodbc` para SQL Server 
* **Generación de diagramas:** Integración con el servidor web de PlantUML. 

## 🛠️ Instalación y Puesta en Marcha

Para ejecutar este proyecto localmente, sigue estos pasos:

### **Requisitos Previos**

* Git
* Node.js (v18 o superior)
* Python (v3.0 o superior)

### **Instrucciones**

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/rooseveltalej/DynamicDBDiagrams.git
    cd DynamicDBDiagrams
    ```

2.  **Configura el Backend:**
    * Navega a la carpeta `backend`:
        ```bash
        cd backend
        ```
    * (Recomendado) Crea y activa un entorno virtual:
        ```bash
        # Para Linux/macOS
        python3 -m venv env
        source env/bin/activate

        # Para Windows
        python -m venv env
        .\env\Scripts\activate
        ```
    * Instala las dependencias de Python:
        ```bash
        pip install -r requirements.txt
        ```
    * Inicia el servidor de FastAPI:
        ```bash
        fastapi dev app/app.py
        ```
    * El backend estará corriendo en `http://localhost:8000`.

3.  **Configura el Frontend:**
    * Abre una **nueva terminal** y navega a la carpeta `frontend`:
        ```bash
        cd frontend
        ```
    * Instala las dependencias de Node.js:
        ```bash
        npm install
        ```
    * Inicia el servidor de desarrollo de React:
        ```bash
        npm run dev
        ```
    * La aplicación se abrirá automáticamente en tu navegador en una dirección como `http://localhost:3000/`.

## 💻 Uso

1.  Abre la aplicación en tu navegador.
2.  En el panel lateral izquierdo ("Configuración de Base de Datos"), introduce los datos de conexión:
    * **Tipo de servidor:** Elige entre MySQL, PostgreSQL o SQL Server.
    * **Host:** La dirección del servidor de tu base de datos.
    * **Puerto:** El puerto de la base de datos (se autocompleta con el valor por defecto si se deja en blanco).
    * **Nombre de usuario y Contraseña.**
    * **Nombre de la base de datos.**
3.  Haz clic en el botón **"Generar"**.
4.  El diagrama UML correspondiente a la estructura de tu base de datos aparecerá en el panel principal.
5.  Los diagramas que generes se añadirán a la lista de "Diagramas Anteriores" para que puedas volver a verlos.

## 🎥 Video de Demostración

*Nota: GitHub Markdown no permite incrustar videos directamente. Haz clic en la imagen para ver el video de instalación y demostración en YouTube.*

[![Video de Demostración del Proyecto](https://img.youtube.com/vi/JJ0H10rvqYM/0.jpg)](https://www.youtube.com/watch?v=JJ0H10rvqYM)
