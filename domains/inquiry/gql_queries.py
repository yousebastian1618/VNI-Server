import strawberry
from typing import List, Optional

from auth.guard import login_required
from .models import Inquiry
from domains.inquiry.gql_types import GQLInquiry
from . import services as inquiry_service


def to_gql_inquiry(inquiry) -> GQLInquiry:
  return GQLInquiry(
    id=inquiry.id,
    first_name=inquiry.first_name,
    last_name=inquiry.last_name,
    email=inquiry.email,
    subject=inquiry.subject,
    message=inquiry.message,
    sent_at=getattr(inquiry, "send_at"),
    resolved=getattr(inquiry, "resolved")
  )


@strawberry.type
class InquiryQueries:
  @strawberry.field
  @login_required
  def inquiries(self, limit: int = 20, offset: int = 0) -> List[GQLInquiry]:
    items = inquiry_service.list_inquiries(limit=limit, offset=offset)
    return [to_gql_inquiry(iq) for iq in items]

  @strawberry.field
  def inquiry(self, uid: strawberry.ID) -> Optional[GQLInquiry]:
    inquiry = inquiry_service.get_inquiry(uid)
    return None if inquiry is None else to_gql_inquiry(inquiry)

  @strawberry.field
  def inquiry_count(self) -> int:
    return Inquiry.query.count()