import uuid
from extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String, DateTime


class Product(db.Model):
  __tablename__ = 'products'

  id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  url: Mapped[str] = mapped_column(String(1000), nullable=False)
  order_index: Mapped[int] = mapped_column(default=0)
  uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)