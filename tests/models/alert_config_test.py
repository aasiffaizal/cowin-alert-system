from models.alert_config import AlertConfig


def test_alert_config_model(db):
    db.query(AlertConfig).limit(1).all()
