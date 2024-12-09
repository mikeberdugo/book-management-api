# Biblioteca API

Esta API gestiona una pequeña biblioteca. Permite realizar operaciones CRUD sobre libros, como agregar, listar, actualizar, eliminar y buscar libros por título o autor. Está desarrollada utilizando FastAPI con PostgreSQL como base de datos y SQLAlchemy como ORM para interactuar con la base de datos.

## Tabla de Contenidos
- [Escenario de la Prueba Técnica](#escenario-de-la-prueba-técnica)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
  - [Instalación local](#instalación-local)
  - [Instalación con Docker](#instalación-con-docker)
- [Ejecutar la API](#ejecutar-la-api)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Evaluación](#evaluación)
- [Contacto](#contacto)

## Escenario de la Prueba Técnica

Desarrollar una API REST utilizando FastAPI para gestionar una pequeña biblioteca. La API debe permitir:

- **Agregar libros:** Título, autor, año de publicación, ISBN.
- **Listar libros:** Todos los libros o filtrados por autor o año.
- **Actualizar información de un libro.**
- **Eliminar un libro.**
- **Buscar libros:** Por título o autor.

## Requisitos

Antes de ejecutar la API, asegúrate de tener instalados los siguientes requisitos:

- **Python 3.11 o superior.**
- **PostgreSQL:** Base de datos relacional para almacenar la información de los libros.
- **Docker (opcional):** Recomendado para contenerización.
- **pip:** Para instalar dependencias.

## Instalación

### Instalación local

1. Clona el repositorio:

   ```bash
   git clone https://github.com/mikeberdugo/book-management-api.git
   cd biblioteca-api
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno necesarias en un archivo `.env`.

5. Crea la base de datos y aplica las migraciones.

### Instalación con Docker

1. Asegúrate de tener Docker instalado y funcionando.
2. Construye y ejecuta los contenedores:

   ```bash
   docker-compose up --build
   ```

## Ejecutar la API

Ejecuta el siguiente comando para iniciar la aplicación:

```bash
uvicorn app.main:app --reload
```

Por defecto, la API estará disponible en `http://127.0.0.1:8000`.

## Estructura del Proyecto

```plaintext
biblioteca_api/
├── app/
│   ├── models.py  # Modelos de datos
│   ├── schemas.py # Esquemas de Pydantic para serialización
│   ├── main.py    # Archivo principal de la aplicación
│   └── tests/     # Pruebas unitarias e integración
├── requirements.txt
├── Dockerfile
└── README.md
```

## Evaluación

### Diseño de la API
- **Endpoints RESTful:** Implementación de operaciones GET, POST, PUT y DELETE.
- **Códigos de estado HTTP:** Uso adecuado para las respuestas.
- **Manejo de errores:** Validación de datos y respuestas claras.

### Modelo de Datos
- **Base de datos:** Diseño adecuado para almacenar información de los libros.
- **ORM:** Uso de SQLAlchemy para mapear las entidades.

### Pruebas
- **Cobertura:** Pruebas unitarias e integración.
- **Endpoints:** Verificación del correcto funcionamiento.

### Documentación
- **Swagger:** Generación automática de documentación interactiva.

### Código
- **Principios SOLID:** Diseño mantenible y escalable.
- **Código limpio:** Estructura organizada y legible.

## Contacto

Si tienes preguntas o deseas contribuir, puedes contactarme en:

- **Nombre:** Mike Berdugo
- **Email:** mike.berdugo@example.com

