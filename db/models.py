import sqlalchemy as db
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


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
    tmstmp = Column(String(128), default=None)
    request_time = Column(String(128), default=None)
    first_response = Column(String(128), default=None)
    second_response = Column(String(128), default=None)