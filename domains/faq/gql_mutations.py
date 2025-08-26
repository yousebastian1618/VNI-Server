from typing import Optional

import strawberry
from graphql import GraphQLError

from extensions import db
from domains.faq.gql_queries import FaqCreateInput, FaqUpdateInput
from domains.faq.gql_types import GQLFaq
from domains.faq.models import Faq


@strawberry.type
class FaqMutations:
  @strawberry.mutation
  def create_faq(self, gql_input: FaqCreateInput) -> GQLFaq:
    new_faq = Faq(
      question=gql_input.question,
      answer=gql_input.answer,
      order_index=gql_input.order_index,
    )
    db.session.add(new_faq)
    db.session.commit()
    return GQLFaq(
      id=new_faq.id,
      question=new_faq.question,
      answer=new_faq.answer,
      order_index=new_faq.order_index
    )

  @strawberry.mutation
  def update_faq(self, gql_input: FaqUpdateInput) -> Optional[GQLFaq]:
    updated_faq = Faq.query.get(gql_input.id)
    if not updated_faq:
      raise GraphQLError(
        'Faq does not exist',
        extensions={"code": "NOT_FOUND", "status": 404}
      )
    if gql_input.question is not None:
      updated_faq.question = gql_input.question
    if gql_input.answer is not None:
      updated_faq.answer = gql_input.answer
    if gql_input.order_index is not None:
      updated_faq.order_index = gql_input.order_index
    db.session.commit()
    return GQLFaq(
      id=updated_faq.id,
      question=updated_faq.question,
      answer=updated_faq.answer,
      order_index=updated_faq.order_index
    )

  @strawberry.mutation
  def delete_faq(self, uid: strawberry.ID) -> bool:
    faq = Faq.query.get(uid)
    if not faq:
      raise GraphQLError(
        "Faq does not exist",
        extensions={"code": "NOT_FOUND", "status": 404}
      )
    db.session.delete(faq)
    db.session.commit()
    return True