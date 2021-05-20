from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class State(Base):
    name = Column(String, nullable=False)
    external_id = Column(Integer, nullable=False)
    districts = relationship("District", back_populates="state")
