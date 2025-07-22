# shared/db/models/applications_models.py
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime, timezone
from shared.db.database import Base

class ApplicationModelDb(Base):
    __tablename__ = 'applications'

    id = Column(Integer, index=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), index=True, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True, nullable=False)
    situation = Column(String, index=False, nullable=False)
    comment = Column(String, index=False, nullable=True)
    updated_at = Column(DateTime, index=False, nullable=False, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, index=False, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_id": self.job_id,
            "company_id": self.company_id,
            "situation": self.situation,
            "comment": self.comment,
            "updated_at": self.updated_at,
            "created_at": self.created_at
        }