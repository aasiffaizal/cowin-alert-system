from db.base import get_table_name, db_session
from sqlalchemy.orm import Session


def test_get_table_name_returns_snake_case():
    assert 'aaa_bbb_ccc' == get_table_name('AaaBbbCcc')
    assert 'dd_ff' == get_table_name('DdFf')


def test_db_session():
    with db_session() as db:
        assert isinstance(db, Session)