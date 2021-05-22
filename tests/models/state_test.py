from db.base import db_session
from models.state import State


def test_state_model():
    with db_session() as db:
        db.query(State).limit(1).all()
