from typing import List, Optional
from extensions import db
from domains.inquiry.models import Inquiry
from helper.index import to_uuid


def list_inquiries(limit: int=20, offset: int = 0) -> List[Inquiry]:
  return Inquiry.query.order_by("id").offset(offset).limit(limit).all()

def get_inquiry(uid) -> Optional[Inquiry]:
  return Inquiry.query.get(to_uuid(uid))

def count_inquiries() -> int:
  return Inquiry.query.count()

def create_inquiry(first_name: str, last_name: str, email: str, subject: str, message: str) -> bool:
  inquiry = Inquiry(
    first_name=first_name,
    last_name=last_name,
    email=email,
    subject=subject,
    message=message
  )
  db.session.add(inquiry)
  db.session.commit()
  return True

def update_inquiry(uid, resolved: bool):
  inquiry = Inquiry.query.get(to_uuid(uid))
  if not inquiry:
    return None
  if resolved is not None: inquiry.resolved = resolved
  db.session.commit()
  return inquiry

def delete_inquiry(uid) -> bool:
  inquiry = Inquiry.query.get(to_uuid(uid))
  if not inquiry:
    return False
  db.session.delete(inquiry)
  db.session.commit()
  return True