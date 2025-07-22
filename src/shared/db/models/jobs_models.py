# shared/db/models/jobs_models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from ..database import Base

class JobModelDb(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, index=True, primary_key=True)
    job_external_id = Column(Integer, index=False, nullable=True)
    job_title = Column(String, index=False, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True, nullable=False)
    country = Column(String, index=False, nullable=False)
    state = Column(String, index=False, nullable=False)
    city = Column(String, index=False, nullable=False)
    neighborhood = Column(String, index=False, nullable=True)
    created_at = Column(DateTime, index=False, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "job_external_id": self.job_external_id,
            "job_title": self.job_title,
            "company_id": self.company_id,
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "neighborhood": self.neighborhood,
            "created_at": self.created_at
        }