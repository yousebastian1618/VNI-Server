import strawberry
from graphql import GraphQLError
from .models import Product
from .gql_types import ProductCreateInput, GQLProduct
from extensions import db


@strawberry.type
class ProductMutations:
  @strawberry.mutation
  def create_product(self, gql_input: ProductCreateInput) -> GQLProduct:
    product = Product(
      url=gql_input.url,
      order_index=gql_input.order_index,
    )
    db.session.add(product)
    db.session.commit()
    return GQLProduct(
      id=product.id,
      url=product.url,
      order_index=product.order_index,
      uploaded_at=product.uploaded_at
    )

  @strawberry.mutation
  def delete_product(self, uid: strawberry.ID) -> bool:
    product = Product.query.get(uid)
    if not product:
      raise GraphQLError(
        'Product not found',
        extensions={"code": "NOT_FOUND", "status": 404}
      )
    db.session.delete(product)
    db.session.commit()
    return True
