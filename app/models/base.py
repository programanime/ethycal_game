from functools import wraps

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session as DBSession
from sqlalchemy.orm import sessionmaker

from app.utils.mixins import AsDictMixin, DatedMixin

DATABASE_URL = "sqlite:///game.db"

CONSTRAINT_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(AsDictMixin, DatedMixin):
    def get_db_session(self):
        return DBSession.object_session(self)


metadata = MetaData(naming_convention=CONSTRAINT_NAMING_CONVENTION)
Base = declarative_base(cls=Base, metadata=metadata)
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def with_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            result = func(*args, **kwargs, db_session=session)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper
