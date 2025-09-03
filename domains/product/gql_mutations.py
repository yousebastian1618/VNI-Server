from __future__ import annotations
from typing import Optional, List
import strawberry
from .gql_types import GQLProduct, ProductUpdateInput, ProductOrderInput
from . import services as product_service



def to_gql_product(product) -> GQLProduct:
  return GQLProduct(
    id=product.id,
    index=getattr(product, "index", 0),
    uploaded_at=getattr(product, "uploaded_at", None),
  )

@strawberry.type
class ProductMutations:
  @strawberry.mutation
  # @login_required
  def create_product(self) -> GQLProduct:
    product = product_service.create_product()
    return to_gql_product(product)

  @strawberry.mutation
  # @login_required
  def update_product(self, gql_input: ProductUpdateInput) -> Optional[GQLProduct]:
    product = product_service.update_product(uid=gql_input.id, index=gql_input.index)
    return None if product is None else to_gql_product(product)

  @strawberry.mutation
  # @login_required
  def reorder_products(self, gql_input: List[ProductOrderInput]) -> bool:
    return product_service.reorder_products(product_index_map=gql_input)

  @strawberry.mutation
  # @login_required
  def delete_product(self, uid: strawberry.ID) -> bool:
    return product_service.delete_product(uid=uid)

  @strawberry.mutation
  # @login_required
  def delete_products(self, uids: List[str]) -> List[GQLProduct]:
    items = product_service.delete_products(uids=uids)
    return [to_gql_product(p) for p in items]


