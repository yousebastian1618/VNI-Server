import strawberry
from auth.guard import login_required
from .gql_types import GQLInquiry, InquiryUpdateInput
from domains.inquiry.gql_types import InquiryCreateInput
from . import services as inquiry_service


def to_gql_inquiry(inquiry) -> GQLInquiry:
  return GQLInquiry(
    id=inquiry.id,
    first_name=inquiry.first_name,
    last_name=inquiry.last_name,
    email=inquiry.email,
    subject=inquiry.subject,
    message=inquiry.message,
    sent_at=inquiry.sent_at,
    resolved=inquiry.resolved,
  )

@strawberry.type
class InquiryMutations:
  @strawberry.mutation
  def create_inquiry(self, gql_input: InquiryCreateInput) -> bool:
    return inquiry_service.create_inquiry(
      first_name=gql_input.first_name,
      last_name=gql_input.last_name,
      email=gql_input.email,
      subject=gql_input.subject,
      message=gql_input.message
    )

  @strawberry.mutation
  @login_required
  def update_inquiry(self, gql_input: InquiryUpdateInput) -> GQLInquiry:
    inquiry = inquiry_service.update_inquiry(uid=gql_input.id, resolved=gql_input.resolved)
    return None if inquiry is None else to_gql_inquiry(inquiry)

  @strawberry.mutation
  @login_required
  def delete_inquiry(self, uid: strawberry.ID) -> bool:
    return inquiry_service.delete_inquiry(uid)