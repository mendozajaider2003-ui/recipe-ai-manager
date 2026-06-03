from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .crud_user import user
from ..models.models import Ingredient, Recipe, Rating
from ..schemas import IngredientCreate, IngredientUpdate, RecipeCreate, RatingCreate

class CRUDBase:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def remove(self, db: Session, *, id: int):
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

class CRUDIngredient(CRUDBase):
    def create_with_owner(self, db: Session, *, obj_in: IngredientCreate, owner_id: int) -> Ingredient:
        db_obj = Ingredient(**obj_in.dict(), usuario_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Ingredient]:
        return db.query(self.model).filter(Ingredient.usuario_id == owner_id).offset(skip).limit(limit).all()

    def update(self, db: Session, *, db_obj: Ingredient, obj_in: IngredientUpdate) -> Ingredient:
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDRecipe(CRUDBase):
    def create_with_owner(self, db: Session, *, obj_in: RecipeCreate, owner_id: int) -> Recipe:
        db_obj = Recipe(**obj_in.dict(), usuario_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Recipe]:
        return db.query(self.model).filter(Recipe.usuario_id == owner_id).offset(skip).limit(limit).all()

    def get_with_rating(self, db: Session, *, owner_id: int):
        recipes = db.query(
            Recipe,
            func.coalesce(func.avg(Rating.puntuacion), 0).label('promedio')
        ).outerjoin(
            Rating, Recipe.id == Rating.receta_id
        ).filter(
            Recipe.usuario_id == owner_id
        ).group_by(
            Recipe.id
        ).all()
        
        result = []
        for recipe, promedio in recipes:
            recipe.calificacion_promedio = float(promedio)
            result.append(recipe)
        return result

class CRUDRating(CRUDBase):
    def create_with_owner(self, db: Session, *, obj_in: RatingCreate, owner_id: int) -> Rating:
        db_obj = Rating(**obj_in.dict(), usuario_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_recipe(self, db: Session, *, recipe_id: int, skip: int = 0, limit: int = 100) -> List[Rating]:
        return db.query(self.model).filter(Rating.receta_id == recipe_id).offset(skip).limit(limit).all()

    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Rating]:
        return db.query(self.model).filter(Rating.usuario_id == owner_id).offset(skip).limit(limit).all()

ingredient = CRUDIngredient(Ingredient)
recipe = CRUDRecipe(Recipe)
rating = CRUDRating(Rating)
