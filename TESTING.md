# Guía de Testing

## Pruebas Unitarias

### Ejecutar Todas las Pruebas

```bash
cd backend
pytest
```

### Ejecutar Pruebas Específicas

```bash
# Pruebas de LLM
pytest tests/test_llm_prompt.py

# Pruebas de API
pytest tests/test_api_recetas.py

# Pruebas de Ingredientes
pytest tests/test_ingredientes.py
```

### Ejecutar con Cobertura

```bash
pytest --cov=app tests/
```

### Ejecutar en Modo Verbose

```bash
pytest -v
```

## Estructura de Pruebas

### test_llm_prompt.py

Pruebas para la generación de recetas con IA:

- `test_construir_prompt_vacio()`: Manejo de lista vacía
- `test_construir_prompt_con_ingredientes()`: Generación con ingredientes
- `test_construir_prompt_con_muchos_ingredientes()`: Manejo de múltiples ingredientes
- `test_resultado_contiene_campos_requeridos()`: Validación de campos
- `test_resultado_json_valido()`: Validación de JSON

### test_api_recetas.py

Pruebas de endpoints:

- `test_read_main()`: Ruta raíz
- `test_login_page()`: Página de login
- `test_register_page()`: Página de registro
- `test_inventory_page()`: Página de inventario
- `test_recipes_page()`: Página de recetas
- `test_api_users_endpoint_exists()`: Endpoint de usuarios
- `test_api_ingredients_endpoint_exists()`: Endpoint de ingredientes
- `test_api_recipes_endpoint_exists()`: Endpoint de recetas
- `test_static_files_mounted()`: Archivos estáticos

### test_ingredientes.py

Pruebas de CRUD de ingredientes:

- `test_crear_usuario()`: Creación de usuario
- `test_obtener_usuario_por_email()`: Obtención de usuario
- `test_usuario_no_existe()`: Manejo de usuario no existente
- `test_crear_ingrediente()`: Creación de ingrediente
- `test_obtener_ingredientes_por_usuario()`: Obtención de ingredientes

## Pruebas Manuales

### Flujo de Registro

1. Acceder a `http://localhost:8000/register`
2. Completar formulario con datos válidos
3. Verificar que se redirige a login
4. Intentar registrarse con email duplicado
5. Verificar mensaje de error

### Flujo de Login

1. Acceder a `http://localhost:8000/login`
2. Ingresar credenciales válidas
3. Verificar que se redirige a inventory
4. Ingresar credenciales inválidas
5. Verificar mensaje de error

### Gestión de Ingredientes

1. Acceder a `/inventory` (debe estar autenticado)
2. Agregar nuevo ingrediente
3. Verificar que aparece en la lista
4. Editar ingrediente
5. Eliminar ingrediente
6. Verificar que se elimina de la lista

### Generación de Recetas

1. Agregar al menos 3 ingredientes
2. Hacer clic en "Generar Receta"
3. Esperar a que se genere
4. Verificar que aparece en `/recipes`
5. Calificar la receta
6. Verificar que se guarda la calificación

## Debugging

### Ver Logs

```bash
docker-compose logs -f app
```

### Ejecutar con Debugger

```bash
# Agregar breakpoint en código
import pdb; pdb.set_trace()

# Ejecutar pytest
pytest -s tests/test_file.py
```

### Base de Datos de Prueba

Las pruebas usan SQLite en memoria. Para usar base de datos real:

```python
# En conftest.py
SQLALCHEMY_DATABASE_URL = "mysql://user:password@localhost/test_db"
```

## CI/CD

### GitHub Actions

Crear `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest
```

## Cobertura de Código

### Generar Reporte

```bash
pytest --cov=app --cov-report=html tests/
```

### Ver Reporte

Abrir `htmlcov/index.html` en el navegador

## Mejores Prácticas

1. Escribir tests para nuevas funcionalidades
2. Mantener cobertura > 80%
3. Usar nombres descriptivos para tests
4. Usar fixtures para datos comunes
5. Aislar tests (no depender de otros)
6. Limpiar datos después de cada test
7. Usar mocks para dependencias externas
8. Documentar tests complejos
# Commit 2 - Validación de Ingredientes
# Laura - Animaciones
