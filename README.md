# TeamKraken API

## Requisitos

- Python 3.9: https://www.python.org/downloads/release/python-390/ (navegar hasta el fondo de la página que abre esta url y descargar el ejecutable correspondiente a su SO).

## Instalación y configuración previa

### Instalación de entorno virtual

- En la carpeta donde se haya descargado el proyecto, crear una carpeta llamada `entornos`.

- Navegar hacia la carpeta entornos y, ahí, ejecutar el comando `python -m venv <nombre-entorno>` para crear un entorno virtual. A efectos de documentación, supondremos que hemos creado un entorno llamado `team-kraken`.

- Aparecerá, dentro de la carpeta `entronos`, un nuevo directorio llamado `teamk-kraken`.

- **EL SIGUIENTE PASO HABRÁ QUE REALIZARLO** **_CADA VEZ_** **QUE QUERAMOS EJECUTAR EL PROYECTO**

- Navegamos hasta el directorio `/team-kraken/Scripts/` y ejecutamos el comando `activate`.

  - En el sistema operativo Linux, basta con, desde la carpeta `entornos`, ejecutar el comando `source /team-kraken/Scripts/activate`.
  - En el sistema operativo Windows, tendremos que hacer los pasos tal y como se han descrito. Es posible que escribir simplemente `activate` resulte un error. En tal caso, escribir `.\activate` en su lugar.

- Una vez activado el entorno, nuestro proyecto funcionará con normalidad siempre.

### Instalación de dependencias

- **MUY IMPORTANTE:** Si estamos trabajando en un sistema operativo Linux, abir el fichero `/requirements/local.txt` y cambiar la entrada `psycopg2==2.9.3` por `psycopg2-binary==2.9.3`. Si estamos en Windows, podemos dejarlo tal y como está.

- Navegar hacia la carpeta `requirements` y ejecutar el comando `pip install -r local.txt`.

### Descarga e instalación de ChromeDriver v102

- Descargar el ejecutable de `ChromeDriver v102` acorde a su sistema operativo del siguiente sitio web: https://chromedriver.storage.googleapis.com/index.html?path=102.0.5005.61/

- Si no se está usando Chrome v102 (si no se sabe cuál es la versión que se está usando, se puede consultar en https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have), puede descargar esta versión del navegador, u optar por utilizar la versión de ChromeDriver acorde a la de su navegador. De no ser compatibles las versiones de ChromeDriver y de Chrome, no se podrá ejecutar ninguna función del scraping.

- **Fundamental:** Descomprimir el zip de ChromeDriver y colocar en la ruta `C:/Windows/chromedriver/chromedriver.exe` el archivo .exe generado.

- Seguir los siguientes pasos en orden:

  - Estando situado en la carpeta `TeamKraken-API-V2`, ejecutar el comando `cd .\TeamKraken\`
  - Una vez en la carpeta TeamKraken (podemos asegurar que estamos en la carpeta correcta ejecutando el comando `dir` (o `ls -la` si estamos en Linux) y comprobar que entre los archivos listados se encuentra el archivo `manage.py`), ejecutar los siguientes tres comandos tal y como se indica:
    1. `python manage.py makemigrations`
    2. `python manage.py migrate`
    3. `python manage.py runserver`

- Una vez hecho esto, nuestro API estará ejecutado y listo para usar desde el socket http://127.0.0.1:8000 (siempre que el puerto 8000 de su equipo esté libre).

### Creación de superusuario para el panel de Administrador de Django

- Estando situado en la carpeta `TeamKraken-API-V2`, ejecutar el comando `cd .\TeamKraken\`

- Una vez en la carpeta TeamKraken (podemos asegurar que estamos en la carpeta correcta ejecutando el comando `dir` (o `ls -la` si estamos en Linux) y comprobar que entre los archivos listados se encuentra el archivo `manage.py`), ejecutar los siguientes pasos tal y como se indica:

  1. `pyhton manage.py createsuperuser`
  2. Introducir nombre de usuario
  3. (OPCIONAL) Introducir un email. Si no se quiere añadir un email, pulsar la tecla `Enter` sin escribir nada
  4. Introducir contraseña
  5. Repetir contraseña

- Hecho esto, acceder a la url http://127.0.0.1:8000/admin e iniciar sesión con el usuario que acabamos de crear.

- Una vez dentro, se pueden consultar las tablas de las bases de datos e interactuar con los mismos como se guste.
