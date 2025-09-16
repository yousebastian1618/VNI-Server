from typing import List, Optional
from domains.inquiry.models import Inquiry
from flask_mail import Message
from extensions import mail, db
from flask import current_app


def send_inquiry(sender_email: str, first_name: str, last_name: str, subject: str, message: str):
  admin_email = current_app.config.get("ADMIN_EMAIL")
  msg = Message(
    subject=subject,
    body=f"From: {first_name + ' ' + last_name} <{sender_email}>\n\n{message}",
    recipients=[admin_email],
    reply_to=sender_email
  )
  mail.send(msg)
  return True

def list_inquiries(limit: int=20, offset: int = 0) -> List[Inquiry]:
  return Inquiry.query.order_by("id").offset(offset).limit(limit).all()

def get_inquiry(uid) -> Optional[Inquiry]:
  return Inquiry.query.get(uid)

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
  send_inquiry(email, first_name, last_name, subject, message)
  db.session.add(inquiry)
  db.session.commit()
  return True

def update_inquiry(uid, resolved: bool):
  inquiry = Inquiry.query.get(uid)
  if not inquiry:
    return None
  if resolved is not None: inquiry.resolved = resolved
  db.session.commit()
  return inquiry

def delete_inquiry(uid) -> bool:
  inquiry = Inquiry.query.get(uid)
  if not inquiry:
    return False
  db.session.delete(inquiry)
  db.session.commit()
  return True