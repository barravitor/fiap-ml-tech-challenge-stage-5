# shared/db/models/companies_models.py
from sqlalchemy import Column, Integer, String
from ..database import Base

class CompanyModelDb(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }