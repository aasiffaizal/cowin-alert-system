from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from db.base import Base
import enum


class Filters(enum.Enum):
    Vaccine = 0
    Age = 1
    Dose = 2


class Evaluators(enum.Enum):
    Equals = '='
    GreaterThan = '>'
    LessThan = '<'
    In = 'in'


class ConfiguredFilter(Base):
    alert_config_id = Column(Integer, ForeignKey('alert_config.id'))
    filter = Column(Enum(Filters), nullable=False)
    evaluator = Column(Enum(Evaluators), nullable=False)
    value = Column(String, nullable=False)
    alert_config = relationship('AlertConfig', back_populates="configured_filters")