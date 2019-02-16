import time
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column
from sqlalchemy import UniqueConstraint
from sqlalchemy import (
    Integer, String, DateTime, Array, LargeBinary
)
from .base import db, Base


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    picture = Column(LargeBinary())
    description = Column(String(2556))
    start_date = Column(DateTime)
    duration = Column(String(80))
