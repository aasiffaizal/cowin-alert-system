from db.base import db_session
from models.alert_config import AlertConfig


def test_alert_config_model():
    with db_session() as db:
        db.query(AlertConfig).limit(1).all()
