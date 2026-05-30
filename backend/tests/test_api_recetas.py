import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_read_main():
    """Prueba que la ruta raíz redirige correctamente."""
    response = client.get("/", allow_redirects=False)
    assert response.status_code == 307  # Redirect


def test_login_page():
    """Prueba que la página de login se carga correctamente."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "Iniciar Sesión" in response.text or "login" in response.text.lower()


def test_register_page():
    """Prueba que la página de registro se carga correctamente."""
    response = client.get("/register")
    assert response.status_code == 200


def test_inventory_page():
    """Prueba que la página de inventario se carga correctamente."""
    response = client.get("/inventory")
    assert response.status_code == 200
    assert "Inventario" in response.text or "inventario" in response.text.lower()


def test_recipes_page():
    """Prueba que la página de recetas se carga correctamente."""
    response = client.get("/recipes")
    assert response.status_code == 200
    assert "Recetas" in response.text or "recetas" in response.text.lower()


def test_api_users_endpoint_exists():
    """Prueba que el endpoint de usuarios existe."""
    response = client.post("/api/v1/users/login", 
        json={"username": "test@example.com", "password": "test"})
    # Puede dar 422 (validation error) o 400, pero el endpoint existe
    assert response.status_code in [200, 400, 422]


def test_api_ingredients_endpoint_exists():
    """Prueba que el endpoint de ingredientes existe."""
    response = client.get("/api/v1/ingredients/")
    # Puede dar 401 (no autenticado) o 200, pero el endpoint existe
    assert response.status_code in [200, 401, 403]


def test_api_recipes_endpoint_exists():
    """Prueba que el endpoint de recetas existe."""
    response = client.get("/api/v1/recipes/")
    # Puede dar 401 (no autenticado) o 200, pero el endpoint existe
    assert response.status_code in [200, 401, 403]


def test_static_files_mounted():
    """Prueba que los archivos estáticos se sirven correctamente."""
    response = client.get("/static/memphis.css")
    assert response.status_code == 200
    assert "background" in response.text or "color" in response.text
