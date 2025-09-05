import uuid
import sqlalchemy as sa
from extensions import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime


class Product(db.Model):
  __tablename__ = 'products'

  id: Mapped[str] = mapped_column(sa.String(36), primary_key=True, default=str(uuid.uuid4()))
  index: Mapped[int] = mapped_column(default=0)
  uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)