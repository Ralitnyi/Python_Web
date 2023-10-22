from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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
    user_id = Column(
        "users_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    user = relationship("User", backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column("crated_at", DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
