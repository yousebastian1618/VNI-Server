import uuid
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from extensions import db


class User(db.Model):
  __tablename__ = "users"

  id: Mapped[str] = mapped_column(sa.String(36), primary_key=True, default=str(uuid.uuid4()))
  email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)


  def set_password(self, password: str):
    self.password = generate_password_hash(password)

  def check_password(self, password: str) -> bool:
    return check_password_hash(self.password, password)
