from models.district import District


def test_district_model(db):
    db.query(District).limit(1).all()
