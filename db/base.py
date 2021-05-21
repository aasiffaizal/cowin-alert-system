import inflection
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declared_attr
from config import APP

CONFIG = APP['database']

DATABASE_URL = CONFIG['url']

# check_same_thread is only needed if the db is sqlite
engine = create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}
)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_table_name(name: str) -> str:
    return inflection.underscore(name)


class BaseModel:

    @declared_attr
    def __tablename__(cls):
        """Convert CamelCase class name to underscores_between_words
        table name.
        """
        return get_table_name(cls.__name__)

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())


Base = declarative_base(cls=BaseModel)
