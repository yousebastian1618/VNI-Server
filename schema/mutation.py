import strawberry
from domains.blog.gql_mutations import BlogMutations
from domains.product.gql_mutations import ProductMutations
from domains.inquiry.gql_mutations import InquiryMutations
from domains.user.gql_mutations import UserMutations
from domains.maintenance.gql_mutations import MaintenanceMutation

@strawberry.type
class Mutation(BlogMutations, ProductMutations, InquiryMutations, UserMutations, MaintenanceMutation):
  @strawberry.mutation
  def ping(self) -> bool:
    return True