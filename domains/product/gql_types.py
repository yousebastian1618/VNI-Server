import strawberry
from datetime import datetime

@strawberry.type
class GQLProduct:
  id: strawberry.ID
  url: str
  index: int = 0
  uploaded_at: datetime

@strawberry.input
class ProductCreateInput:
  url: str
  index: int = 0

