import sqlalchemy as db
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class TcpInfo(Base):
    __tablename__ = 'tcp'

    id = Column(Integer, primary_key=True)
    name = Column(String, default=None)
    host = Column(String, default=None)
    port = Column(Integer, default=None)
    first_query = Column(String, default=None)
    second_query = Column(String, default=None)
    timeout = Column(Integer, default=None)
    request_interval = Column(Integer, default=None)
    create_time = Column(DateTime, default=datetime.now)

class TcpResult(Base):
    __tablename__ = 'tcp_result'

    id = Column(Integer, primary_key=True)
    name = Column(String, default=None)
    status = Column(String, default=None)
    tmstmp = Column(String, default=None)
    request_time = Column(String, default=None)
    first_response = Column(String, default=None)
    second_response = Column(String, default=None)
    create_time = Column(DateTime, default=datetime.now)