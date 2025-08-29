import uuid
from datetime import datetime
from extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class Blog(db.Model):
  __tablename__ = 'blogs'

  id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  title: Mapped[str] = mapped_column(String(200), nullable=True)
  subtitle: Mapped[str] = mapped_column(String(300), nullable=True)
  main_image: Mapped[str] = mapped_column(String(1000), nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
  index: Mapped[int] = mapped_column(default=0)
  images: Mapped[list["BlogImage"]] = relationship("BlogImage", back_populates="blog", cascade="all, delete-orphan", order_by="BlogImage.index")
  paragraphs: Mapped[list["BlogParagraph"]] = relationship("BlogParagraph", back_populates="blog", cascade="all, delete-orphan", order_by="BlogParagraph.index")


class BlogImage(db.Model):
  __tablename__ = "blog_images"

  id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  blog_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("blogs.id", ondelete="CASCADE"))
  url: Mapped[str] = mapped_column(String(1000), nullable=False)
  alt_text: Mapped[str] = mapped_column(String(300), nullable=True, default="")
  index: Mapped[int] = mapped_column(default=0)
  blog: Mapped[Blog] = relationship("Blog", back_populates="images")

class BlogParagraph(db.Model):
  __tablename__ = "blog_paragraphs"

  id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  blog_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("blogs.id", ondelete="CASCADE"))
  text: Mapped[str] = mapped_column(Text, nullable=False)
  index: Mapped[int] = mapped_column(default=0)
  blog: Mapped[Blog] = relationship("Blog", back_populates="paragraphs")
