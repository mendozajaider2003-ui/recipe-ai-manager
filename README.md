# Recipe AI Manager

Esta es una aplicación web completa para gestionar tu inventario de ingredientes y generar recetas creativas utilizando Inteligencia Artificial (OpenRouter).

## Requisitos
- Docker y Docker Compose
- Una instancia externa de MySQL (o PostgreSQL)
- Una API Key de [OpenRouter](https://openrouter.ai/)

## Configuración
1. Clona este repositorio.
2. Copia el archivo `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edita el archivo `.env` con tus credenciales de base de datos y tu API Key de OpenRouter.

## Ejecución con Docker
Para levantar la aplicación, simplemente ejecuta:
```bash
docker-compose up --build
```

La aplicación estará disponible en `http://localhost:8000`.

## Inicializar Base de Datos
Una vez que el contenedor esté corriendo, puedes crear las tablas ejecutando:
```bash
docker exec -it recipe_app_container python init_db.py
```

## Estructura del Proyecto
- `backend/`: Código fuente de la API con FastAPI.
  - `app/api/`: Endpoints de la aplicación.
  - `app/models/`: Modelos de SQLAlchemy.
  - `app/schemas/`: Esquemas de Pydantic.
  - `app/templates/`: Vistas HTML con Jinja2.
  - `app/core/`: Configuración, seguridad y LLM.
- `docker-compose.yml`: Orquestación de contenedores.
# Commit 7 - Rate Limiting
