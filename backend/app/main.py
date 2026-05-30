from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api.v1 import api_router
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Permitir solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos (CSS, JS, imágenes)
import os
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configurar Jinja2Templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

app.include_router(api_router, prefix=settings.API_V1_STR)

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    # Reutilizamos el login para simplificar la demo o podrías crear register.html
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("inventory.html", {"request": request, "ingredients": []})

@app.get("/inventory", response_class=HTMLResponse)
async def inventory_page(request: Request):
    return templates.TemplateResponse("inventory.html", {"request": request, "ingredients": []})

@app.get("/recipes", response_class=HTMLResponse)
async def recipes_page(request: Request):
    return templates.TemplateResponse("recipes.html", {"request": request, "recipes": []})

@app.post("/login")
async def login_post(request: Request):
    """Procesar formulario de login."""
    try:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")
        
        # Aquí iría la lógica de autenticación real
        # Por ahora, redirigir al inventario
        return RedirectResponse(url="/inventory", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/login", status_code=303)

@app.post("/register")
async def register_post(request: Request):
    """Procesar formulario de registro."""
    try:
        form = await request.form()
        email = form.get("email")
        password = form.get("password")
        nombre = form.get("nombre")
        
        # Aquí iría la lógica de registro real
        # Por ahora, redirigir al login
        return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/register", status_code=303)

@app.post("/inventory")
async def add_ingredient(request: Request):
    """Añadir un ingrediente al inventario."""
    try:
        form = await request.form()
        nombre = form.get("nombre")
        cantidad = form.get("cantidad")
        
        # Aquí iría la lógica para guardar el ingrediente
        # Por ahora, redirigir al inventario
        return RedirectResponse(url="/inventory", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/inventory", status_code=303)

@app.post("/inventory/delete/{ingredient_id}")
async def delete_ingredient(ingredient_id: int, request: Request):
    """Eliminar un ingrediente del inventario."""
    try:
        # Aquí iría la lógica para eliminar el ingrediente
        # Por ahora, redirigir al inventario
        return RedirectResponse(url="/inventory", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/inventory", status_code=303)

@app.get("/generate-recipe")
async def generate_recipe_page(request: Request):
    """Generar una receta con IA."""
    try:
        # Aquí iría la lógica para generar la receta
        # Por ahora, redirigir a las recetas
        return RedirectResponse(url="/recipes", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/inventory", status_code=303)

@app.post("/recipes/delete/{recipe_id}")
async def delete_recipe(recipe_id: int, request: Request):
    """Eliminar una receta del historial."""
    try:
        # Aquí iría la lógica para eliminar la receta
        # Por ahora, redirigir a las recetas
        return RedirectResponse(url="/recipes", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/recipes", status_code=303)

@app.post("/recipes/{recipe_id}/rate")
async def rate_recipe(recipe_id: int, request: Request):
    """Calificar una receta."""
    try:
        data = await request.json()
        puntuacion = data.get("puntuacion")
        
        # Aquí iría la lógica para guardar la calificación
        # Por ahora, redirigir a las recetas
        return RedirectResponse(url="/recipes", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/recipes", status_code=303)

@app.get("/logout")
async def logout():
    """Cerrar sesión."""
    return RedirectResponse(url="/login", status_code=303)

