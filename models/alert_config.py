from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class AlertConfig(Base):
    district_id = Column(Integer, ForeignKey('district.id'))
    chat_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    configured_filters = relationship("ConfiguredFilter", back_populates="alert_config")
    district = relationship('District', back_populates="alert_configs")


