from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from db import models

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

SyncSession = sessionmaker(bind=engine)
models.Base.metadata.create_all(engine)
with SyncSession() as session:
    first = {
        "host": '176.113.83.95',
        "port": 22,
        "timeout": 3,
        "request_interval": 3,
        "first_request": 'bim',
        "second_request": 'ueiekn',
        "name": 'Server A'
    }
    second = {
        "host": '45.141.102.225',
        "port": 22,
        "timeout": 3,
        "request_interval": 3,
        "first_request": 'poe',
        "second_request": 'bsjs',
        "name": 'Server b'
    }
    session.add(models.TcpInfo(**first))
    session.add(models.TcpInfo(**second))
    session.commit()