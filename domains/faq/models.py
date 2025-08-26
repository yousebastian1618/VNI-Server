import uuid
from extensions import db
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Text

class Faq(db.Model):
  __tablename__ = "faqs"

  id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  question: Mapped[str] = mapped_column(Text, nullable=False)
  answer: Mapped[str] = mapped_column(Text, nullable=False)
  order_index: Mapped[int] = mapped_column(default=0)