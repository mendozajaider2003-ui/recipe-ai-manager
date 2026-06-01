from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import crud, schemas
from ....dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Rating)
def create_rating(
    *,
    db: Session = Depends(get_db),
    rating_in: schemas.RatingCreate,
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    recipe = crud.recipe.get(db, id=rating_in.recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    rating = crud.rating.create_with_owner(db, obj_in=rating_in, owner_id=current_user.id)
    return rating

@router.get("/recipe/{recipe_id}", response_model=List[schemas.Rating])
def read_ratings_for_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    ratings = crud.rating.get_multi_by_recipe(db, recipe_id=recipe_id, skip=skip, limit=limit)
    return ratings

@router.get("/user/{user_id}", response_model=List[schemas.Rating])
def read_ratings_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    if user_id != current_user.id and not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ratings = crud.rating.get_multi_by_owner(db, owner_id=user_id, skip=skip, limit=limit)
    return ratings

@router.delete("/{id}", response_model=schemas.Rating)
def delete_rating(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    rating = crud.rating.get(db, id=id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    if not crud.user.is_superuser(current_user) and (rating.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    rating = crud.rating.remove(db, id=id)
    return rating
