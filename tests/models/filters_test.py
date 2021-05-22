from db.base import db_session
from models.filters import ConfiguredFilter


def test_filters_model():
    with db_session() as db:
        db.query(ConfiguredFilter).limit(1).all()
