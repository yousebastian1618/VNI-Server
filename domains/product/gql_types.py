import strawberry
from datetime import datetime
from typing import Optional

@strawberry.type
class GQLProduct:
  id: strawberry.ID
  index: int = 0
  uploaded_at: datetime

@strawberry.input
class ProductUpdateInput:
    id: strawberry.ID
    index: Optional[int] = None

@strawberry.input
class ProductOrderInput:
    id: strawberry.ID
    index: int