import uuid
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from extensions import db

class Maintenance(db.Model):
  __tablename__ = 'maintenance'

  id: Mapped[str] = mapped_column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  maintenance: Mapped[bool] = mapped_column(default=False)

