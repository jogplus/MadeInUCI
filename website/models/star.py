import time
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column
from sqlalchemy import UniqueConstraint
from sqlalchemy import (
    Integer, String
)
from .base import db, Base


class Star(Base):
    __tablename__ = 'star'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    projectid = Column(Integer)
