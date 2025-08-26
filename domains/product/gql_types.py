import strawberry
from datetime import datetime

@strawberry.type
class GQLProduct:
  id: strawberry.ID
  url: str
  order_index: int = 0
  uploaded_at: datetime

@strawberry.input
class ProductCreateInput:
  url: str
  order_index: int = 0

