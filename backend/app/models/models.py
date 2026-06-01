from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ingredientes = relationship("Ingredient", back_populates="owner")
    recetas = relationship("Recipe", back_populates="owner")
    calificaciones = relationship("Rating", back_populates="owner")

class Ingredient(Base):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nombre = Column(String(100), nullable=False)
    cantidad = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="ingredientes")

class Recipe(Base):
    __tablename__ = "recetas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nombre = Column(String(200), nullable=False)
    ingredientes_json = Column(JSON, nullable=False)
    pasos_json = Column(JSON, nullable=False)
    tiempo = Column(String(50))
    dificultad = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="recetas")
    calificaciones = relationship("Rating", back_populates="receta")

class Rating(Base):
    __tablename__ = "calificaciones"
    id = Column(Integer, primary_key=True, index=True)
    receta_id = Column(Integer, ForeignKey("recetas.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    puntuacion = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="calificaciones")
    receta = relationship("Recipe", back_populates="calificaciones")
