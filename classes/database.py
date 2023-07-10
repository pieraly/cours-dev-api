from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://steph_render:ZIPWG5kTQqhuqrLWtZLQWAg08VLD2MHY@dpg-ci8rmv18g3n3vm6clj9g-a.frankfurt-postgres.render.com/jerseys'

# Équivalent à une "connexion"
database_engine = create_engine(DATABASE_URL)

# Équivalent à un "curseur"
Session = sessionmaker(bind=database_engine, autocommit=False, autoflush=False)

# get_db est utilisée par presque tous les points de terminaison pour se connecter à la base de données
def get_cursor():
    db = Session()
    try:
        yield db
    finally:
        db.close()
