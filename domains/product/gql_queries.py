import strawberry
from .gql_types import GQLProduct
from typing import List
from .models import Product
from typing import Optional

@strawberry.type
class ProductQueries:
  @strawberry.field
  def products(self, limit: int = 20, offset: int = 0) -> List[GQLProduct]:
    rows = Product.query.order_by(Product.uploaded_at.desc()).offset(offset).limit(limit)
    return [
      GQLProduct(
        id=p.id,
        url=p.url,
        order_index=p.order_index,
        uploaded_at=p.uploaded_at
      ) for p in rows
    ]

  @strawberry.field
  def product(self, uid: strawberry.ID) -> Optional[GQLProduct]:
    product = Product.query.get(uid)
    if not product:
      return None
    return GQLProduct(
      id=product.id,
      url=product.url,
      order_index=product.order_index,
      uploaded_at=product.uploaded_at
    )

  @strawberry.field
  def count_products(self) -> int:
    return Product.query.count()