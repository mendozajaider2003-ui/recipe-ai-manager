from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import crud, schemas
from ....dependencies import get_db, get_current_user
from ....core.llm import generate_recipe_from_ingredients

router = APIRouter()

@router.post("/generate", response_model=schemas.Recipe)
def generate_recipe(
    *,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    ingredients = crud.ingredient.get_multi_by_owner(db, owner_id=current_user.id)
    if not ingredients:
        raise HTTPException(status_code=400, detail="No ingredients in your inventory to generate a recipe.")
    
    ingredient_names = [ing.nombre for ing in ingredients]
    recipe_data = generate_recipe_from_ingredients(ingredient_names)
    
    recipe_in = schemas.RecipeCreate(
        nombre=recipe_data["nombre"],
        ingredientes_json=recipe_data["ingredientes_json"],
        pasos_json=recipe_data["pasos_json"],
        tiempo=recipe_data["tiempo"],
        dificultad=recipe_data["dificultad"],
    )
    recipe = crud.recipe.create_with_owner(db, obj_in=recipe_in, owner_id=current_user.id)
    return recipe

@router.get("/", response_model=List[schemas.Recipe])
def read_recipes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    recipes = crud.recipe.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return recipes

@router.delete("/{id}", response_model=schemas.Recipe)
def delete_recipe(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    recipe = crud.recipe.get(db, id=id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if not crud.user.is_superuser(current_user) and (recipe.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    recipe = crud.recipe.remove(db, id=id)
    return recipe
