from __future__ import annotations
from typing import List, Optional
import strawberry
from .gql_types import GQLProduct
from . import services as product_service

def to_gql_product(p) -> GQLProduct:
    return GQLProduct(
        id=p.id,
        index=getattr(p, "index", 0),
        uploaded_at=getattr(p, "uploaded_at")
    )

@strawberry.type
class ProductQueries:
    @strawberry.field
    def products(self) -> List[GQLProduct]:
        items = product_service.list_products()
        return [to_gql_product(p) for p in items]

    @strawberry.field
    def product(self, uid: strawberry.ID) -> Optional[GQLProduct]:
        p = product_service.get_product(uid)
        return None if p is None else to_gql_product(p)

    @strawberry.field
    def products_count(self) -> int:
        return product_service.count_products()
