from app import db
from sqlalchemy import CHAR, VARCHAR, NUMERIC, DATETIME, Column, INTEGER

class Request(db.Model):
    __tablename__ = 'syn-flood'

    ID = Column(INTEGER, primary_key = True)
    src_mac = Column(CHAR(17))
    dst_mac = Column(CHAR(17))
    src_ip = Column(CHAR(15))
    dst_ip = Column(CHAR(15))
    prot_ip = Column(VARCHAR(10))
    is_syn = Column(NUMERIC(1))
    time = Column(DATETIME)