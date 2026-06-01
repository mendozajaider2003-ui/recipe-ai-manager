from app.models.models import Base
from app.dependencies import engine

def init_db():
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas con éxito.")

if __name__ == "__main__":
    init_db()
