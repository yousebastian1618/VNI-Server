import strawberry
from typing import List, Optional
from .models import Faq
from domains.faq.gql_types import GQLFaq


@strawberry.type
class FaqQueries:
  @strawberry.field
  def faqs(self, limit: int = 20, offset: int = 0) -> List[GQLFaq]:
    rows = Faq.query.order_by(Faq.order_index).offset(offset).limit(limit)
    return [
      GQLFaq(
        id=f.id,
        question=f.question,
        answer=f.answer,
        order_index=f.order_index
      ) for f in rows
    ]

  @strawberry.field
  def faq(self, uid: strawberry.ID) -> Optional[GQLFaq]:
    fq = Faq.query.get(id=uid)
    if not fq:
      return None
    return GQLFaq(
      id=fq.id,
      question=fq.question,
      answer=fq.answer,
      order_index=fq.order_index
    )

  @strawberry.field
  def faq_count(self) -> int:
    return Faq.query.count()


@strawberry.input
class FaqCreateInput:
  question: str
  answer: str
  order_index: int = 0

@strawberry.input
class FaqUpdateInput:
  question: str
  answer: str
  order_index: int = 0
