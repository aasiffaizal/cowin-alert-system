from typing import Optional
import os
from sqlalchemy import Table, Column, String, Integer, MetaData, TIMESTAMP, func
import alembic.config
from db.base import Base
from schemas.base import BaseSchema
from crud.base import CRUDBase
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import APP
CONFIG = APP['test']

ALEMBIC_ARGS = [
    '--raiseerr',
    '-x', 'dbPath={}'.format(CONFIG['database']['url']),
    'upgrade', 'head',
]
TEST_DB_PATH = CONFIG['database']['path']

engine = create_engine(
    CONFIG['database']['url'], connect_args={'check_same_thread': False}
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestTable(Base):
    name = Column(String, nullable=False)
    test_string = Column(String)
    test_int = Column(Integer)


class TestSchema(BaseSchema):
    name: str
    test_string: Optional[str]
    test_int: Optional[int]

    class Config:
        orm_mode = True


def delete_test_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture(scope='session')
def db():
    yield Session()


@pytest.fixture(scope='function')
def db_with_add(db, monkeypatch):
    monkeypatch.setattr(db, 'commit', db.flush)
    yield db
    db.rollback()


@pytest.fixture(autouse=True, scope='session')
def setup_db(db):
    delete_test_db()
    alembic.config.main(argv=ALEMBIC_ARGS)
    meta = MetaData()
    test_table = Table(
        'test_table', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('test_string', String),
        Column('test_int', Integer),
        Column('created_at', TIMESTAMP, default=func.now()),
        Column('updated_at', TIMESTAMP, default=func.now(), onupdate=func.now())
    )
    meta.create_all(engine)
    yield
    delete_test_db()


@pytest.fixture(scope='session')
def test_model():
    yield TestTable


@pytest.fixture(scope='session')
def test_schema():
    yield TestSchema


@pytest.fixture(scope='session')
def test_crud(test_model):
    yield CRUDBase(test_model)


