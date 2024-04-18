from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP


class AsDictMixin:
    def as_dict(self):
        return {
            column: getattr(self, column) for column in self.__mapper__.columns.keys()
        }


class DatedMixin:
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP, nullable=True)
