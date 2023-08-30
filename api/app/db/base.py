from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, func
from datetime import datetime

Base = declarative_base() # faz ligacao de tudo, das nossas models com nosso ORM em si.

class TrackTimeMixin:
    created_at = Column('created_at', DateTime, server_default=func.now())
    updated_at = Column('updated_at', DateTime, onupdate=func.now())

class SoftDeleteMixin:
    deleted_at = Column('deleted_at', DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()