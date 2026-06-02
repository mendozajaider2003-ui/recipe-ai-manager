# Guía de Solución de Problemas

## Problemas Comunes

### Puerto 8000 ya en uso

**Error:**
```
Address already in use
```

**Solución:**

Opción 1: Cambiar puerto en docker-compose.yml
```yaml
ports:
  - "8001:8000"
```

Opción 2: Liberar el puerto
```bash
# En Linux/Mac
lsof -ti:8000 | xargs kill -9

# En Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error de conexión a base de datos

**Error:**
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError)
```

**Solución:**

1. Verificar que MySQL está corriendo
2. Verificar credenciales en `.env`
3. Verificar que la base de datos existe
4. Verificar conectividad de red

```bash
# Probar conexión
docker exec recipe_app_container mysql -h db -u user -p -e "SELECT 1"
```

### Errores de dependencias

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solución:**

```bash
# Reinstalar dependencias
cd backend
pip install -r requirements.txt

# O con Docker
docker-compose down
docker-compose up --build --no-cache
```

### Errores de migración de base de datos

**Error:**
```
sqlalchemy.exc.ProgrammingError
```

**Solución:**

```bash
# Recrear base de datos
docker exec recipe_app_container python init_db.py

# O manualmente
docker exec recipe_app_container mysql -h db -u user -p -e "DROP DATABASE recipe_db; CREATE DATABASE recipe_db;"
```

### Problemas de autenticación

**Error:**
```
401 Unauthorized
```

**Solución:**

1. Verificar que el token JWT es válido
2. Verificar que la cookie se está enviando
3. Verificar que SECRET_KEY es correcto
4. Limpiar cookies del navegador

```bash
# En navegador
localStorage.clear()
sessionStorage.clear()
```

### Problemas con OpenRouter LLM

**Error:**
```
openrouter.exceptions.AuthenticationError
```

**Solución:**

1. Verificar que OPENROUTER_API_KEY está configurada
2. Verificar que la API Key es válida
3. Verificar que tienes créditos disponibles
4. Verificar conectividad de red

```bash
# Probar API Key
curl -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": "test"}]}'
```

### Errores de templates Jinja2

**Error:**
```
jinja2.exceptions.TemplateNotFound
```

**Solución:**

1. Verificar que el archivo template existe
2. Verificar la ruta del directorio de templates
3. Verificar permisos de archivo

```bash
# Verificar templates
ls -la backend/app/templates/

# Verificar permisos
chmod 644 backend/app/templates/*.html
```

### Problemas de CSS/Static Files

**Error:**
```
404 Not Found para /static/memphis.css
```

**Solución:**

1. Verificar que los archivos estáticos existen
2. Verificar que StaticFiles está montado correctamente
3. Limpiar caché del navegador

```bash
# Verificar archivos
ls -la backend/app/static/

# Limpiar caché
Ctrl+Shift+Delete en navegador
```

### Errores de CORS

**Error:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solución:**

Actualizar CORS en main.py:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Problemas de rendimiento

**Síntoma:**
```
Aplicación lenta
```

**Solución:**

1. Verificar logs de base de datos
2. Agregar índices a tablas
3. Optimizar queries
4. Aumentar recursos de Docker

```bash
# Ver logs
docker-compose logs app

# Aumentar memoria
# En docker-compose.yml
services:
  app:
    mem_limit: 2g
```

### Errores de pytest

**Error:**
```
ImportError: cannot import name 'app'
```

**Solución:**

1. Verificar que pytest.ini está configurado
2. Verificar PYTHONPATH
3. Verificar que __init__.py existe en directorios

```bash
# Ejecutar desde backend
cd backend
pytest

# O establecer PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest
```

## Logs Útiles

### Ver logs en tiempo real

```bash
docker-compose logs -f app
```

### Ver logs de base de datos

```bash
docker-compose logs -f db
```

### Guardar logs en archivo

```bash
docker-compose logs app > app.log
```

## Reset Completo

Si todo falla, hacer reset completo:

```bash
# Detener contenedores
docker-compose down

# Eliminar volúmenes
docker-compose down -v

# Limpiar imágenes
docker system prune -a

# Reconstruir
docker-compose up --build
```

## Contacto y Soporte

Si el problema persiste:

1. Revisar GitHub Issues
2. Crear nuevo GitHub Issue con:
   - Descripción del problema
   - Pasos para reproducir
   - Logs relevantes
   - Versión de Docker
   - Sistema operativo
