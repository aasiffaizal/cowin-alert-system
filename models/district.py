from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class District(Base):
    state_id = Column(Integer, ForeignKey('state.id'))
    name = Column(String, nullable=False)
    external_id = Column(Integer, nullable=False)
    state = relationship('State', back_populates="districts")
    alert_configs = relationship("AlertConfig", back_populates="district")
