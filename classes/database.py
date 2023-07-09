from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://igor_render:5lGQuN1kIVPqR4x6GD7a7Z7EpW9ja2GQ@dpg-ci8rn3h8g3nfuca2vvc0-a.frankfurt-postgres.render.com/shop_wapi_render'

# Équivalent à une "connexion"
database_engine = create_engine(DATABASE_URL)

# Équivalent à un "curseur"
Session = sessionmaker(bind=database_engine, autocommit=False, autoflush=False)

# get_db est utilisée par presque tous les points de terminaison pour se connecter à la base de données
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
