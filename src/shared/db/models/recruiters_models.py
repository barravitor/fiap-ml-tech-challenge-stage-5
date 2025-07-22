# shared/db/models/recruiters_models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from shared.db.database import Base

class RecruiterModelDb(Base):
    __tablename__ = 'recruiters'

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=False, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, index=False, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True, nullable=False)
    created_at = Column(DateTime, index=False, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "company_id": self.company_id,
            "created_at": self.created_at
        }