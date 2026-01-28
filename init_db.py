from database.models import Base
from database.connection import engine

def init_database():
    Base.metadata.create_all(engine)
    print("all database-tables were created successfully")

if __name__ == "__main__":
    init_database()
