from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String(50), unique=True)
    phone = Column(String(50), unique=True)
    birthday = Column(DateTime)
    description = Column(String(150), nullable=True)
