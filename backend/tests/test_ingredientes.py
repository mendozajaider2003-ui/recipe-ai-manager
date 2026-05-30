import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, Ingrediente, Usuario
from app.crud.crud_user import user as crud_user
from app.schemas import UserCreate


# Crear base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Fixture que proporciona una sesión de base de datos para pruebas."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_crear_usuario(db):
    """Prueba que se puede crear un usuario."""
    user_data = UserCreate(email="test@example.com", password="testpass", nombre="Test User")
    usuario = crud_user.create(db, obj_in=user_data)
    
    assert usuario.email == "test@example.com"
    assert usuario.nombre == "Test User"
    assert usuario.hashed_password != "testpass"  # Debe estar hasheado


def test_obtener_usuario_por_email(db):
    """Prueba que se puede obtener un usuario por email."""
    user_data = UserCreate(email="test@example.com", password="testpass", nombre="Test User")
    usuario_creado = crud_user.create(db, obj_in=user_data)
    
    usuario_obtenido = crud_user.get_by_email(db, email="test@example.com")
    
    assert usuario_obtenido is not None
    assert usuario_obtenido.email == usuario_creado.email


def test_usuario_no_existe(db):
    """Prueba que retorna None cuando el usuario no existe."""
    usuario = crud_user.get_by_email(db, email="noexiste@example.com")
    assert usuario is None


def test_crear_ingrediente(db):
    """Prueba que se puede crear un ingrediente."""
    # Primero crear un usuario
    user_data = UserCreate(email="test@example.com", password="testpass", nombre="Test User")
    usuario = crud_user.create(db, obj_in=user_data)
    
    # Crear ingrediente
    ingrediente = Ingrediente(
        usuario_id=usuario.id,
        nombre="Tomate",
        cantidad="500g"
    )
    db.add(ingrediente)
    db.commit()
    db.refresh(ingrediente)
    
    assert ingrediente.nombre == "Tomate"
    assert ingrediente.cantidad == "500g"
    assert ingrediente.usuario_id == usuario.id


def test_obtener_ingredientes_por_usuario(db):
    """Prueba que se pueden obtener los ingredientes de un usuario."""
    # Crear usuario
    user_data = UserCreate(email="test@example.com", password="testpass", nombre="Test User")
    usuario = crud_user.create(db, obj_in=user_data)
    
    # Crear ingredientes
    for nombre in ["Tomate", "Cebolla", "Ajo"]:
        ingrediente = Ingrediente(
            usuario_id=usuario.id,
            nombre=nombre,
            cantidad="100g"
        )
        db.add(ingrediente)
    db.commit()
    
    # Obtener ingredientes
    ingredientes = db.query(Ingrediente).filter(Ingrediente.usuario_id == usuario.id).all()
    
    assert len(ingredientes) == 3
    assert all(ing.usuario_id == usuario.id for ing in ingredientes)
