# Biblioteca API

Esta API gestiona una pequeña biblioteca. Permite realizar operaciones CRUD sobre libros, como agregar, listar, actualizar, eliminar y buscar libros por título o autor. Está desarrollada utilizando **FastAPI** con **PostgreSQL** como base de datos y **SQLAlchemy** como ORM para interactuar con la base de datos.

---

## Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Instalación](#instalación)
   - [Instalación local](#instalación-local)
   - [Instalación con Docker](#instalación-con-docker)
3. [Ejecutar la API](#ejecutar-la-api)
4. [Endpoints de la API](#endpoints-de-la-api)
5. [Pruebas](#pruebas)
6. [Contribución](#contribución)
7. [Licencia](#licencia)
8. [Contacto](#contacto)

---

## Requisitos

Antes de ejecutar la API, asegúrate de tener instalados los siguientes requisitos:

- **Python 3.11** o superior.
- **PostgreSQL** (para la base de datos).
- **Docker** (opcional, pero recomendado para contenerización).
- **pip** (para instalar dependencias).

---

## Instalación

### Instalación local

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/mikeberdugo/book-management-api.git
   cd biblioteca-api
