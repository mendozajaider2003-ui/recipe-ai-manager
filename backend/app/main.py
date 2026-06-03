from fastapi import FastAPI, Depends, HTTPException, Request, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import os
import json

from .api.v1 import api_router
from .core.config import settings
from .dependencies import get_db
from .crud.crud_user import user as crud_user
from .crud import ingredient as crud_ingredient, recipe as crud_recipe, rating as crud_rating
from .core.security import create_access_token
from .schemas import UserCreate, IngredientCreate, RatingCreate, RecipeCreate

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configurar templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

app.include_router(api_router, prefix=settings.API_V1_STR)


def get_user_from_token(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        from jose import jwt
        token = token.replace("Bearer ", "")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = crud_user.get_by_email(db, email=payload.get("sub"))
        return user
    except:
        return None


# ========== PÁGINAS LIMPIAS (SIN NAVBAR) ==========

@app.get("/login_clean", response_class=HTMLResponse)
async def login_clean_page(request: Request, error: str = None):
    return templates.TemplateResponse("login_clean.html", {"request": request, "error": error})

@app.get("/register_clean", response_class=HTMLResponse)
async def register_clean_page(request: Request, error: str = None):
    return templates.TemplateResponse("register_clean.html", {"request": request, "error": error})

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/login_clean")


# ========== RUTAS DE AUTENTICACIÓN ==========

@app.post("/login")
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = crud_user.authenticate(db, email=username, password=password)
    if not user:
        return templates.TemplateResponse(
            "login_clean.html", 
            {"request": request, "error": "Email o contraseña incorrectos"}
        )
    access_token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/inventory", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.post("/register")
async def register_post(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = crud_user.get_by_email(db, email=email)
    if existing_user:
        return templates.TemplateResponse(
            "register_clean.html", 
            {"request": request, "error": "El email ya está registrado"}
        )
    
    user_in = UserCreate(nombre=nombre, email=email, password=password)
    crud_user.create(db, obj_in=user_in)
    return RedirectResponse(url="/login_clean", status_code=303)


# ========== RUTAS PROTEGIDAS (REQUIEREN LOGIN) ==========

@app.get("/inventory", response_class=HTMLResponse)
async def inventory_page(request: Request, db: Session = Depends(get_db)):
    user = get_user_from_token(request, db)
    if not user:
        return RedirectResponse(url="/login_clean", status_code=303)
    
    ingredientes = crud_ingredient.get_multi_by_owner(db, owner_id=user.id)
    return templates.TemplateResponse("inventory.html", {"request": request, "ingredientes": ingredientes})


@app.post("/inventory")
async def add_ingredient(
    request: Request,
    nombre: str = Form(...),
    cantidad: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_user_from_token(request, db)
    if not user:
        return RedirectResponse(url="/login_clean", status_code=303)
    
    ingredient_in = IngredientCreate(nombre=nombre, cantidad=cantidad)
    crud_ingredient.create_with_owner(db, obj_in=ingredient_in, owner_id=user.id)
    return RedirectResponse(url="/inventory", status_code=303)


@app.post("/inventory/delete/{ingredient_id}")
async def delete_ingredient(
    ingredient_id: int, 
    request: Request, 
    db: Session = Depends(get_db)
):
    user = get_user_from_token(request, db)
    if not user:
        return RedirectResponse(url="/login_clean", status_code=303)
    
    crud_ingredient.remove(db, id=ingredient_id)
    return RedirectResponse(url="/inventory", status_code=303)


@app.post("/inventory/edit/{ingredient_id}")
async def edit_ingredient(
    ingredient_id: int,
    request: Request,
    nombre: str = Form(...),
    cantidad: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_user_from_token(request, db)
    if not user:
        return RedirectResponse(url="/login_clean", status_code=303)
    
    ingredient = crud_ingredient.get(db, id=ingredient_id)
    if ingredient and ingredient.usuario_id == user.id:
        ingredient.nombre = nombre
        ingredient.cantidad = cantidad
        db.commit()
    
    return RedirectResponse(url="/inventory", status_code=303)


@app.get("/recipes", response_class=HTMLResponse)
async def recipes_page(request: Request, db: Session = Depends(get_db)):
    user = get_user_from_token(request, db)
    if not user:
        return RedirectResponse(url="/login_clean", status_code=303)
    
    recetas = crud_recipe.get_multi_by_owner(db, owner_id=user.id)
    return templates.TemplateResponse("recipes.html", {"request": request, "recetas": recetas})


@app.get("/generate-recipe")
async def generate_recipe(request: Request, db: Session = Depends(get_db)):
    user = get_user_from_token(request, db)
    if not user:
        return RedirectResponse(url="/login_clean", status_code=303)
    
    ingredientes = crud_ingredient.get_multi_by_owner(db, owner_id=user.id)
    if not ingredientes:
        return RedirectResponse(url="/inventory", status_code=303)
    
    from .core.llm import generate_recipe_from_ingredients
    
    ingredient_names = [ing.nombre for ing in ingredientes]
    recipe_data = generate_recipe_from_ingredients(ingredient_names)
    
    recipe_in = RecipeCreate(
        nombre=recipe_data["nombre"],
        ingredientes_json=recipe_data["ingredientes_json"],
        pasos_json=recipe_data["pasos_json"],
        tiempo=recipe_data["tiempo"],
        dificultad=recipe_data["dificultad"],
    )
    crud_recipe.create_with_owner(db, obj_in=recipe_in, owner_id=user.id)
    
    return RedirectResponse(url="/recipes", status_code=303)


@app.post("/recipes/delete/{recipe_id}")
async def delete_recipe(
    recipe_id: int, 
    request: Request, 
    db: Session = Depends(get_db)
):
    user = get_user_from_token(request, db)
    if not user:
        return RedirectResponse(url="/login_clean", status_code=303)
    
    crud_recipe.remove(db, id=recipe_id)
    return RedirectResponse(url="/recipes", status_code=303)


@app.post("/recipes/{recipe_id}/rate")
async def rate_recipe(
    recipe_id: int, 
    request: Request, 
    db: Session = Depends(get_db)
):
    user = get_user_from_token(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    body = await request.body()
    data = json.loads(body)
    puntuacion = data.get("puntuacion")
    
    rating_in = RatingCreate(receta_id=recipe_id, puntuacion=puntuacion)
    crud_rating.create_with_owner(db, obj_in=rating_in, owner_id=user.id)
    
    return {"message": "Calificación guardada"}


@app.get("/recipes/{recipe_id}", response_class=HTMLResponse)
async def recipe_detail_page(request: Request, recipe_id: int, db: Session = Depends(get_db)):
    user = get_user_from_token(request, db)
    if not user:
        return RedirectResponse(url="/login_clean", status_code=303)
    
    receta = crud_recipe.get(db, id=recipe_id)
    if not receta:
        return RedirectResponse(url="/recipes", status_code=303)
    
    ingredientes = json.loads(receta.ingredientes_json) if isinstance(receta.ingredientes_json, str) else receta.ingredientes_json
    pasos = json.loads(receta.pasos_json) if isinstance(receta.pasos_json, str) else receta.pasos_json
    
    return templates.TemplateResponse(
        "recipe_detail.html", 
        {"request": request, "receta": receta, "ingredientes": ingredientes, "pasos": pasos}
    )


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login_clean")
    response.delete_cookie("access_token")
    return response


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    user = get_user_from_token(request, db)
    if not user:
        return RedirectResponse(url="/login_clean", status_code=303)
    
    return RedirectResponse(url="/inventory")
