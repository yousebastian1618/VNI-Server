import strawberry
from graphql import GraphQLError
from .gql_types import GQLBlog
from typing import List
from .models import Blog
from . import services as blog_service

def to_gql_blog(blog) -> GQLBlog:
  return GQLBlog(
    id=blog.id,
    title=blog.title,
    subtitle=blog.subtitle,
    created_at=blog.created_at,
    updated_at=blog.updated_at,
    index=blog.index,
    images=blog.images,
    paragraphs=blog.paragraphs
  )

@strawberry.type
class BlogQueries:
  @strawberry.field
  def blogs(self, limit: int = 20, offset: int = 0) -> List[GQLBlog]:
    items = blog_service.list_blogs(limit=limit, offset=offset)
    return [to_gql_blog(b) for b in items]

  @strawberry.field
  def blog(self, uid: strawberry.ID) -> GQLBlog:
    blog = blog_service.blog(uid)
    if not blog:
      raise GraphQLError(
        "Blog not found",
        extensions={"code": "NOT_FOUND", "status": 404}
      )
    return to_gql_blog(blog)

  @strawberry.field
  def count_blogs(self) -> int:
    return Blog.query.count()