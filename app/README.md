# Invera ToDo-List Challenge

## Descripción
Aplicación ToDo List para Challenge técnico en Invera.

## Requisitos previos
- Python 3.11+
- pip
- (Opcional) Docker y Docker Compose

## Instalación y ejecución local
# Usuario cargado
- User: admin
- Password: admin

1. **Crea y activa un entorno virtual:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Aplica las migraciones:**
   ```sh
   python manage.py migrate
   ```

5. **Crea un superusuario (opcional, para acceder al admin):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Inicia el servidor:**
   ```sh
   python manage.py runserver
   ```

7. **Accede a la aplicación:**
   - Navega a [http://localhost:8000](http://localhost:8000)

---

## Ejecución con Docker
# Usuario cargado
- User: admin
- Password: admin


1. **Construye la imagen:**
   ```sh
   docker build -t invera-todo-app .
   ```

2. **Ejecuta el contenedor:**
   ```sh
   docker run --name invera-todo-container -p 8000:8000 invera-todo-app
   ```

3. **Accede a la aplicación:**
   - Navega a [http://localhost:8000](http://localhost:8000)

---

## Pruebas

1. **Para ejecutar los tests:**
    ```sh
    python manage.py test
    ```

---

## Notas
- Puedes modificar la configuración en [`app/app/settings.py`](app/app/settings.py).
- La base de datos por defecto es SQLite (`db.sqlite3`).
