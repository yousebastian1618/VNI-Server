import strawberry

@strawberry.type
class GQLFaq:
  id: strawberry.ID
  question: str
  answer: str
  index: int = 0