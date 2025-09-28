import strawberry
from domains.blog.gql_queries import BlogQueries
from domains.product.gql_queries import ProductQueries
from domains.inquiry.gql_queries import InquiryQueries
from domains.user.gql_queries import UserQueries
from domains.maintenance.gql_queries import MaintenanceQueries

@strawberry.type
class Query(BlogQueries, ProductQueries, InquiryQueries, UserQueries, MaintenanceQueries):
  @strawberry.field
  def health(self) -> str:
    return "ok"