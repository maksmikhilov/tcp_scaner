from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.automap import automap_base
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=False,
)
inspector = inspect(engine)
print(inspector.get_columns('book'))