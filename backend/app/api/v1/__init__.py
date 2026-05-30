from fastapi import APIRouter

from .endpoints import users, ingredients, recipes, ratings

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(ingredients.router, prefix="/ingredients", tags=["ingredients"])
api_router.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
