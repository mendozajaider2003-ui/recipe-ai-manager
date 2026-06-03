from typing import List, Optional, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    nombre: str
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

# Ingredient schemas
class IngredientBase(BaseModel):
    nombre: Optional[str] = None
    cantidad: Optional[str] = None

class IngredientCreate(IngredientBase):
    nombre: str
    cantidad: str

class IngredientUpdate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int
    usuario_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Recipe schemas
class RecipeBase(BaseModel):
    nombre: Optional[str] = None
    ingredientes_json: Optional[Any] = None
    pasos_json: Optional[Any] = None
    tiempo: Optional[str] = None
    dificultad: Optional[str] = None

class RecipeCreate(RecipeBase):
    nombre: str
    ingredientes_json: Any
    pasos_json: Any

class RecipeUpdate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    usuario_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Rating schemas

class RatingBase(BaseModel):
    puntuacion: Optional[int] = None
    receta_id: Optional[int] = None

class RatingCreate(RatingBase):
    receta_id: int
    puntuacion: int

class Rating(RatingBase):
    id: int
    usuario_id: int
    created_at: datetime

    class Config:
        from_attributes = True
