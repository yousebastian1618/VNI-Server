import strawberry
from domains.blog.gql_queries import BlogQueries
from domains.product.gql_queries import ProductQueries
from domains.faq.gql_queries import FaqQueries
from domains.inquiry.gql_queries import InquiryQueries

@strawberry.type
class Query(BlogQueries, ProductQueries, FaqQueries, InquiryQueries):
  @strawberry.field
  def health(self) -> str:
    return "ok"