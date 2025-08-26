import strawberry

@strawberry.type
class GQLFaq:
  id: strawberry.ID
  question: str
  answer: str
  order_index: int = 0