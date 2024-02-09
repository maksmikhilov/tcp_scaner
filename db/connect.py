from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=False,
)
Base = automap_base()
Base.prepare(engine, reflect=True)