import time
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column
from sqlalchemy import UniqueConstraint
from sqlalchemy import (
    Integer, String, DateTime, Array
)
from .base import db, Base


class Stars(Base):
    __tablename__ = 'stars'

    id = Column(Integer, primary_key=True)
    userID = Column(Integer)
    projectID = Column(Integer)