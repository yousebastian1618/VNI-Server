import strawberry
from graphql import GraphQLError
from extensions import db
from .models import Inquiry
from .gql_types import GQLInquiry
from domains.inquiry.gql_types import InquiryCreateInput


@strawberry.type
class InquiryMutations:
  @strawberry.mutation
  def create_inquiry(self, gql_input: InquiryCreateInput) -> GQLInquiry:
    new_inquiry = GQLInquiry(
      first_name=gql_input.first_name,
      last_name=gql_input.last_name,
      email=gql_input.email,
      subject=gql_input.subject,
      text=gql_input.text
    )
    db.session.add(new_inquiry)
    db.session.commit()
    return new_inquiry

  @strawberry.mutation
  def delete_inquiry(self, uid: strawberry.ID) -> bool:
    the_inquiry = Inquiry.query.get(uid)
    if not the_inquiry:
      raise GraphQLError(
        "Inquiry not found",
        extensions={"code": "NOT_FOUND", "status": 404}
      )
    db.session.delete(the_inquiry)
    db.session.commit()
    return True