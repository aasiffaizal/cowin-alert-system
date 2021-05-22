from models.filters import ConfiguredFilter


def test_filters_model(db):
    db.query(ConfiguredFilter).limit(1).all()
