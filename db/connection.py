from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.automap import automap_base
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=False,
)
Base = automap_base()
Base.prepare(engine, reflect=True)
Tcp_table = Base.classes.tcp
print(Tcp_table)
inspector = inspect(engine)
print(inspector.get_columns('tcp'))