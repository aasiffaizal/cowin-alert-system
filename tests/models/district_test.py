from db.base import db_session
from models.district import District


def test_district_model():
    with db_session() as db:
        db.query(District).limit(1).all()
