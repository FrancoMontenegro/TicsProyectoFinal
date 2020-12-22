# Tecnologías

 * HTML
 * CSS3
 * POSTGRES


# Uso de archivos

* run.py : Inicia la aplicación en Flask
* app/setup.py : Estructura BDD
* app/views.py : Lógica para cada ruta específica
* app/seed.py : Encargado de rellenar de datos la BDD respectiva
* app/config.py : Variables de configuración para conexión a BDD

# Metodos (Buenas prácticas)

- GET : Obtener, muestra datos en la URL
- POST : Crear
- DELETE : Borrar
- PUT : Actualizar


# Instalación

* Crear ambiente e instalar Flask: https://flask.palletsprojects.com/en/1.1.x/installation/
* Clonar repositorio
* Verificar si tira error reload(sys) (desde Python 3.4 no se usa)
* Instalar psycopg2: pip install psycopg2-binary
