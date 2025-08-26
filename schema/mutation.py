import strawberry
from domains.blog.gql_mutations import BlogMutations
from domains.product.gql_mutations import ProductMutations
from domains.faq.gql_mutations import FaqMutations
from domains.inquiry.gql_mutations import InquiryMutations

@strawberry.type
class Mutation(BlogMutations, ProductMutations, FaqMutations, InquiryMutations):
  @strawberry.mutation
  def ping(self) -> bool:
    return True