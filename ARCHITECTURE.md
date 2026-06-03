# Arquitectura del Proyecto

## Descripción General

Recipe AI Manager es una aplicación web de gestión de recetas con inteligencia artificial. La arquitectura está diseñada para ser escalable, mantenible y fácil de entender.

## Componentes Principales

### Backend (FastAPI)

El backend está construido con FastAPI y proporciona:

- **API REST**: Endpoints para CRUD de ingredientes, recetas y calificaciones
- **Autenticación JWT**: Seguridad basada en tokens
- **Integración LLM**: Generación de recetas con OpenRouter
- **Base de Datos**: MySQL con SQLAlchemy ORM

### Frontend (Jinja2 + HTML/CSS)

El frontend utiliza:

- **Templates Jinja2**: Renderizado dinámico de HTML
- **Bootstrap 5**: Framework CSS responsivo
- **CSS Personalizado**: Diseño Memphis vibrante
- **Formularios HTML**: Interacción con el usuario

### Base de Datos

Estructura de tablas:

```
usuarios
├── id (PK)
├── nombre
├── email (UNIQUE)
├── hashed_password
└── created_at

ingredientes
├── id (PK)
├── usuario_id (FK)
├── nombre
├── cantidad
└── created_at

recetas
├── id (PK)
├── usuario_id (FK)
├── nombre
├── ingredientes_json
├── pasos_json
├── tiempo
├── dificultad
└── created_at

calificaciones
├── id (PK)
├── receta_id (FK)
├── usuario_id (FK)
├── puntuacion
└── created_at
```

## Flujo de Datos

### Registro e Inicio de Sesión

1. Usuario envía formulario de registro/login
2. Backend valida credenciales
3. Si es válido, genera JWT
4. JWT se almacena en cookie httpOnly
5. Usuario es redirigido a /inventory

### Gestión de Ingredientes

1. Usuario accede a /inventory
2. Backend obtiene ingredientes del usuario autenticado
3. Usuario puede agregar/editar/eliminar ingredientes
4. Cambios se persisten en base de datos

### Generación de Recetas

1. Usuario hace clic en "Generar Receta"
2. Backend obtiene ingredientes del usuario
3. Envía ingredientes a OpenRouter LLM
4. LLM genera receta en formato JSON
5. Receta se guarda en base de datos
6. Usuario es redirigido a /recipes

### Calificación de Recetas

1. Usuario selecciona puntuación (1-5 estrellas)
2. Envía POST a /recipes/{id}/rate
3. Backend valida autenticación
4. Guarda calificación en base de datos
5. Retorna confirmación

## Estructura de Directorios

```
recipe_app/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── llm.py
│   │   ├── crud/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── main.py
│   │   └── dependencies.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── pytest.ini
├── docker-compose.yml
├── .env.example
└── README.md
```

## Patrones de Diseño

### CRUD Operations

Cada entidad (Usuario, Ingrediente, Receta, Calificación) tiene:
- Create: Crear nuevo registro
- Read: Obtener registros
- Update: Modificar registro existente
- Delete: Eliminar registro

### Autenticación

- JWT en cookies httpOnly
- Validación en cada ruta protegida
- Tokens con expiración

### Manejo de Errores

- Validación de entrada con Pydantic
- Manejo de excepciones HTTP
- Mensajes de error claros

## Seguridad

- Contraseñas hasheadas con bcrypt
- JWT para autenticación
- CORS configurado
- SQL Injection prevención con ORM
- XSS prevention con Jinja2

## Escalabilidad

- Arquitectura modular
- Separación de concerns
- Base de datos externa
- Contenedorización con Docker
- Fácil de agregar nuevas funcionalidades

## Rendimiento

- Índices en base de datos
- Caché de sesiones
- Queries optimizadas
- Lazy loading de datos

## Testing

- Pruebas unitarias con pytest
- Cobertura de endpoints
- Pruebas de CRUD
- Pruebas de integración LLM
# Commit 3 - Cache de Recetas
# Laura - Responsive
