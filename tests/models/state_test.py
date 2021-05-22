from models.state import State


def test_state_model(db):
    db.query(State).limit(1).all()
