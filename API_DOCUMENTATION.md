# Documentación de API

## Base URL

```
http://localhost:8000/api/v1
```

## Autenticación

Todos los endpoints protegidos requieren un JWT válido en la cookie `access_token`.

## Endpoints

### Usuarios

#### Registro
```
POST /users/register
Content-Type: application/json

{
  "nombre": "string",
  "email": "string",
  "password": "string"
}

Response: 200 OK
{
  "id": 1,
  "nombre": "string",
  "email": "string",
  "created_at": "2024-01-15T10:30:00"
}
```

#### Login
```
POST /users/login
Content-Type: application/json

{
  "email": "string",
  "password": "string"
}

Response: 200 OK
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### Ingredientes

#### Listar Ingredientes
```
GET /ingredients/
Authorization: Bearer {token}

Response: 200 OK
[
  {
    "id": 1,
    "usuario_id": 1,
    "nombre": "Tomate",
    "cantidad": "500g",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### Crear Ingrediente
```
POST /ingredients/
Authorization: Bearer {token}
Content-Type: application/json

{
  "nombre": "string",
  "cantidad": "string"
}

Response: 201 Created
{
  "id": 1,
  "usuario_id": 1,
  "nombre": "string",
  "cantidad": "string",
  "created_at": "2024-01-15T10:30:00"
}
```

#### Actualizar Ingrediente
```
PUT /ingredients/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "nombre": "string",
  "cantidad": "string"
}

Response: 200 OK
{
  "id": 1,
  "usuario_id": 1,
  "nombre": "string",
  "cantidad": "string",
  "created_at": "2024-01-15T10:30:00"
}
```

#### Eliminar Ingrediente
```
DELETE /ingredients/{id}
Authorization: Bearer {token}

Response: 200 OK
{
  "message": "Ingrediente eliminado"
}
```

### Recetas

#### Listar Recetas
```
GET /recipes/
Authorization: Bearer {token}

Response: 200 OK
[
  {
    "id": 1,
    "usuario_id": 1,
    "nombre": "Ensalada de Tomate",
    "ingredientes_json": "[...]",
    "pasos_json": "[...]",
    "tiempo": 15,
    "dificultad": "Fácil",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### Generar Receta
```
POST /recipes/generate
Authorization: Bearer {token}
Content-Type: application/json

{
  "ingredientes": ["Tomate", "Cebolla"]
}

Response: 201 Created
{
  "id": 1,
  "usuario_id": 1,
  "nombre": "string",
  "ingredientes_json": "[...]",
  "pasos_json": "[...]",
  "tiempo": 30,
  "dificultad": "Medio",
  "created_at": "2024-01-15T10:30:00"
}
```

#### Eliminar Receta
```
DELETE /recipes/{id}
Authorization: Bearer {token}

Response: 200 OK
{
  "message": "Receta eliminada"
}
```

### Calificaciones

#### Crear Calificación
```
POST /ratings/
Authorization: Bearer {token}
Content-Type: application/json

{
  "receta_id": 1,
  "puntuacion": 5
}

Response: 201 Created
{
  "id": 1,
  "receta_id": 1,
  "usuario_id": 1,
  "puntuacion": 5,
  "created_at": "2024-01-15T10:30:00"
}
```

#### Obtener Calificaciones de Receta
```
GET /ratings/recipe/{recipe_id}
Authorization: Bearer {token}

Response: 200 OK
[
  {
    "id": 1,
    "receta_id": 1,
    "usuario_id": 1,
    "puntuacion": 5,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

## Códigos de Estado

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Solicitud inválida
- `401 Unauthorized`: Autenticación requerida
- `403 Forbidden`: Acceso denegado
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Errores

Todas las respuestas de error incluyen:

```json
{
  "detail": "Descripción del error"
}
```

## Rate Limiting

No hay rate limiting implementado actualmente.

## Versionado

La API está versionada en `/api/v1`. Futuras versiones estarán disponibles en `/api/v2`, etc.
# Commit 4 - Índices BD
