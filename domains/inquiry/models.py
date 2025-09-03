import uuid
from extensions import db
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Boolean
from datetime import datetime


class Inquiry(db.Model):
  __tablename__ = "inquiries"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  first_name: Mapped[str] = mapped_column(String(50), nullable=True)
  last_name: Mapped[str] = mapped_column(String(50), nullable=True)
  email: Mapped[str]= mapped_column(String(100), nullable=False)
  subject: Mapped[str] = mapped_column(String(100), nullable=False)
  message: Mapped[str] = mapped_column(Text, nullable=False)
  sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
  resolved: Mapped[bool] = mapped_column(Boolean, default=False)


