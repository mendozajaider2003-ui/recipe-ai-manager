# Guía de Despliegue

## Despliegue Local con Docker

### Requisitos Previos

- Docker instalado (versión 20.10+)
- Docker Compose instalado (versión 1.29+)
- Git instalado

### Pasos de Despliegue

1. **Clonar el repositorio**
```bash
git clone https://github.com/mendozajaider2003-ui/recipe-ai-manager.git
cd recipe-ai-manager
```

2. **Configurar variables de entorno**
```bash
cp backend/.env.example backend/.env
# Editar backend/.env con tus credenciales
```

3. **Construir e iniciar los contenedores**
```bash
docker-compose up --build
```

4. **Inicializar la base de datos**
```bash
docker exec -it recipe_app_container python init_db.py
```

5. **Acceder a la aplicación**
Abre tu navegador en `http://localhost:8000`

### Variables de Entorno Requeridas

- `DATABASE_URL`: URL de conexión a MySQL
- `OPENROUTER_API_KEY`: API Key de OpenRouter
- `SECRET_KEY`: Clave secreta para JWT
- `PROJECT_NAME`: Nombre del proyecto

### Ejecutar Pruebas

```bash
docker exec -it recipe_app_container pytest
```

### Detener los Contenedores

```bash
docker-compose down
```

## Despliegue en Producción

### Usando Clever Cloud

1. Crear cuenta en Clever Cloud
2. Crear base de datos MySQL
3. Configurar variables de entorno
4. Conectar repositorio Git
5. Desplegar automáticamente

### Usando Railway

1. Crear cuenta en Railway
2. Conectar repositorio GitHub
3. Configurar variables de entorno
4. Railway desplegará automáticamente

### Usando Render

1. Crear cuenta en Render
2. Crear nuevo servicio web
3. Conectar repositorio
4. Configurar build y start commands
5. Desplegar

## Monitoreo y Mantenimiento

### Logs

Ver logs de la aplicación:
```bash
docker-compose logs -f app
```

### Backup de Base de Datos

```bash
docker exec recipe_app_container mysqldump -u user -p database > backup.sql
```

### Restaurar Base de Datos

```bash
docker exec -i recipe_app_container mysql -u user -p database < backup.sql
```

## Troubleshooting

### Puerto 8000 ya en uso

```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"
```

### Error de conexión a base de datos

Verificar que las credenciales en `.env` sean correctas y que la base de datos esté corriendo.

### Errores de dependencias

```bash
docker-compose down
docker-compose up --build --no-cache
```

## Seguridad

- Cambiar `SECRET_KEY` en producción
- Usar HTTPS en producción
- Configurar CORS apropiadamente
- Usar variables de entorno para credenciales
- Mantener dependencias actualizadas
