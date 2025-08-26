import strawberry
from typing import List, Optional
from .models import Inquiry
from domains.inquiry.gql_types import GQLInquiry


@strawberry.type
class InquiryQueries:
  @strawberry.field
  def inquiries(self, limit: int = 20, offset: int = 0) -> List[GQLInquiry]:
    rows = Inquiry.query.order_by(Inquiry.sent_at.desc()).limit(limit).offset(offset)
    return [
      GQLInquiry(
        id=i.id,
        first_name=i.first_name,
        last_name=i.last_name,
        email=i.email,
        subject=i.subject,
        text=i.text,
        sent_at=i.sent_at,
        resolved=i.resolved
      ) for i in rows
    ]

  @strawberry.field
  def inquiry(self, uid: strawberry.ID) -> Optional[GQLInquiry]:
    the_inquiry = Inquiry.query.get(uid)
    if not the_inquiry:
      return None
    return GQLInquiry(
      id=the_inquiry.id,
      first_name=the_inquiry.first_name,
      last_name=the_inquiry.last_name,
      email=the_inquiry.email,
      subject=the_inquiry.subject,
      text=the_inquiry.text,
      sent_at=the_inquiry.sent_at,
      resolved=the_inquiry.resolved
    )

  @strawberry.field
  def inquiry_count(self) -> int:
    return Inquiry.query.count()