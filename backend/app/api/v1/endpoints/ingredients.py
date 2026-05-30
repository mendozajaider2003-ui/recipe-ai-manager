from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import crud, schemas
from ....dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Ingredient)
def create_ingredient(
    *,
    db: Session = Depends(get_db),
    ingredient_in: schemas.IngredientCreate,
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    ingredient = crud.ingredient.create_with_owner(db, obj_in=ingredient_in, owner_id=current_user.id)
    return ingredient

@router.get("/", response_model=List[schemas.Ingredient])
def read_ingredients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    ingredients = crud.ingredient.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return ingredients

@router.put("/{id}", response_model=schemas.Ingredient)
def update_ingredient(
    *,
    db: Session = Depends(get_db),
    id: int,
    ingredient_in: schemas.IngredientUpdate,
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    ingredient = crud.ingredient.get(db, id=id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    if not crud.user.is_superuser(current_user) and (ingredient.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ingredient = crud.ingredient.update(db, db_obj=ingredient, obj_in=ingredient_in)
    return ingredient

@router.delete("/{id}", response_model=schemas.Ingredient)
def delete_ingredient(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    ingredient = crud.ingredient.get(db, id=id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    if not crud.user.is_superuser(current_user) and (ingredient.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ingredient = crud.ingredient.remove(db, id=id)
    return ingredient
