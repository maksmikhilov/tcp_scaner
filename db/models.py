import sqlalchemy as db
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, create_engine

from datetime import datetime
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

Base = declarative_base()
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
Base.metadata.create_all(engine)

class TcpInfo(Base):
    __tablename__ = 'tcp_info'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), default=None)
    host = Column(String(20), default=None)
    port = Column(Integer, default=None)
    first_request = Column(String(128), default=None)
    second_request = Column(String(128), default=None)
    timeout = Column(Integer, default=None)
    request_interval = Column(Integer, default=None)

class TcpResult(Base):
    __tablename__ = 'tcp_result'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), default=None)
    status = Column(String(128), default=None)
    tmstmp = Column(Float, default=None)
    request_time = Column(Float, default=None)
    connect_time = Column(Float, default=None)
    first_response = Column(Text, default=None)
    second_response = Column(Text, default=None)

"""
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
with Session() as session:
    table = session.query(TcpInfo)
    if not list(table.all()):
        first = {
            "host": '176.134.76.95',
            "port": 22,
            "timeout": 3,
            "request_interval": 3,
            "first_request": 'bim',
            "second_request": 'ueiekn',
            "name": 'Server A'
        }
        second = {
            "host": '45.141.112.222',
            "port": 22,
            "timeout": 3,
            "request_interval": 3,
            "first_request": 'poe',
            "second_request": 'bsjs',
            "name": 'Server b'
        }
        session.add(TcpInfo(**first))
        session.add(TcpInfo(**second))
        session.commit()
"""