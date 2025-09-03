import uuid
from extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID
from sqlalchemy import DateTime


class Product(db.Model):
  __tablename__ = 'products'

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  index: Mapped[int] = mapped_column(default=0)
  uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)